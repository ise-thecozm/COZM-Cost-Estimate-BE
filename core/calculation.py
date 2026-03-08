"""
Port of calculateScenario, calculateTaxLiability, and calculateSS from App.tsx.
All currency amounts stay in the inputCurr unless explicitly converted.
"""
import math
from .constants import LOCATIONS, TIER_BENEFITS, EXCHANGE_RATES, has_totalization_agreement

_ZERO_TAX = {
    'grossIncome': 0, 'deductions': 0, 'netTaxableIncome': 0,
    'stateDeductions': 0, 'stateNetTaxableIncome': 0,
    'brackets': [], 'stateBrackets': [], 'credits': [],
    'totalTax': 0, 'effectiveRate': 0,
    'amounts': {'federal': 0, 'state': 0, 'local': 0},
}

LOCAL_TIERS = {'Local', 'Local Plus'}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _get_country(code):
    return next((c for c in LOCATIONS if c['code'] == code), None)


def _get_city(country_code, city_code):
    default = {'code': 'UNK', 'name': 'Unknown', 'avgTax': 0, 'colaIndex': 100,
               'stateTaxRate': 0, 'localTaxRate': 0}
    country = _get_country(country_code)
    if not country:
        return default
    cities = country.get('cities', [])
    city = next((c for c in cities if c['code'] == city_code), None)
    return city or (cities[0] if cities else default)


def _get_country_name(code):
    c = _get_country(code)
    return c['name'] if c else code


# ---------------------------------------------------------------------------
# Social Security
# ---------------------------------------------------------------------------

def calculate_ss(country_code, income, is_employer):
    country = _get_country(country_code)
    if not country:
        return 0
    if country_code == 'US':
        cap = country.get('socialSecurityCap', 184500)
        medicare_rate = 0.0145
        combined = country.get('socialSecurityRateEmployer' if is_employer else 'socialSecurityRateEmployee', 0)
        oasdi = max(0, combined - medicare_rate)
        return min(income, cap) * oasdi + income * medicare_rate
    rate = country.get('socialSecurityRateEmployer' if is_employer else 'socialSecurityRateEmployee', 0)
    cap = country.get('socialSecurityCap', 0)
    basis = min(income, cap) if cap > 0 else income
    return basis * rate


# ---------------------------------------------------------------------------
# Tax Liability
# ---------------------------------------------------------------------------

def _scale_bracket(bracket, from_curr, to_curr, convert_fn):
    b = dict(bracket)
    b['min'] = convert_fn(b['min'], from_curr, to_curr)
    b['max'] = convert_fn(b['max'], from_curr, to_curr) if b.get('max') is not None else None
    b['taxableAmount'] = convert_fn(b.get('taxableAmount', 0), from_curr, to_curr)
    b['taxDue'] = convert_fn(b.get('taxDue', 0), from_curr, to_curr)
    return b


def _calculate_tax_liability(gross_income, country_code, city_code,
                              marital_status, num_children_under_17, num_children_over_17):
    zero = dict(_ZERO_TAX, grossIncome=gross_income, netTaxableIncome=gross_income)
    if not country_code:
        return zero

    country = _get_country(country_code)
    city = _get_city(country_code, city_code)

    if not country or not country.get('taxBrackets'):
        return zero

    is_married = marital_status in ('Married (Single Income)', 'Married (Dual Income)')

    # Choose brackets
    if is_married and country.get('taxBracketsJoint'):
        tax_brackets = country['taxBracketsJoint']
    else:
        tax_brackets = country['taxBrackets']

    # Standard deduction
    if is_married and country.get('standardDeductionJoint') is not None:
        std_deduction = country['standardDeductionJoint']
    else:
        std_deduction = country.get('standardDeduction', 0)

    # UK: taper personal allowance
    if country_code == 'UK':
        standard_pa = 12570
        effective_pa = standard_pa
        if gross_income > 100000:
            reduction = (gross_income - 100000) / 2
            effective_pa = max(0, standard_pa - reduction)
        std_deduction = effective_pa

    net_taxable = max(0, gross_income - std_deduction)
    federal_tax = 0
    brackets_result = []

    for bracket in tax_brackets:
        min_b = bracket['min']
        max_b = bracket.get('max')
        rate = bracket['rate']
        taxable_amount = 0

        if net_taxable > min_b:
            if max_b is None:
                taxable_amount = net_taxable - min_b
            else:
                taxable_amount = min(net_taxable, max_b) - min_b
                if taxable_amount < 0:
                    taxable_amount = 0

        tax_due = taxable_amount * rate
        federal_tax += tax_due

        if max_b is None or net_taxable > min_b or (min_b == 0 and max_b is not None and max_b > 0):
            brackets_result.append({
                'min': min_b, 'max': max_b, 'rate': rate,
                'taxableAmount': taxable_amount, 'taxDue': tax_due,
            })

    credits = []

    if country_code == 'US':
        # Child Tax Credit
        if num_children_under_17 > 0:
            ctc = 2200
            refundable_limit = 1700
            threshold = 400000 if is_married else 200000
            excess = max(0, gross_income - threshold)
            reduction = math.ceil(excess / 1000) * 50
            max_credit = max(0, num_children_under_17 * ctc - reduction)
            if max_credit > 0:
                non_refundable = min(max(0, federal_tax), max_credit)
                remaining = max_credit - non_refundable
                refundable = min(remaining, num_children_under_17 * refundable_limit)
                if non_refundable > 0:
                    credits.append({'name': 'Child Tax Credit (Non-Refundable)', 'amount': non_refundable})
                if refundable > 0:
                    credits.append({'name': "Addt'l Child Tax Credit (Refundable)", 'amount': refundable})
                federal_tax -= non_refundable + refundable

        # Credit for Other Dependents
        if num_children_over_17 > 0:
            threshold = 400000 if is_married else 200000
            excess = max(0, gross_income - threshold)
            reduction = math.ceil(excess / 1000) * 50
            total_odc = max(0, num_children_over_17 * 500 - reduction)
            if federal_tax > 0 and total_odc > 0:
                usable = min(federal_tax, total_odc)
                if usable > 0:
                    credits.append({'name': 'Credit for Other Dependents', 'amount': usable})
                    federal_tax -= usable

    # State tax
    if is_married and city.get('stateStandardDeductionJoint') is not None:
        state_deduction = city['stateStandardDeductionJoint']
    else:
        state_deduction = city.get('stateStandardDeduction', 0)

    state_taxable = max(0, gross_income - state_deduction)
    state_tax = 0
    state_brackets_result = []

    if is_married and city.get('stateTaxBracketsJoint'):
        state_brackets = city['stateTaxBracketsJoint']
    else:
        state_brackets = city.get('stateTaxBrackets', [])

    if state_brackets:
        for bracket in state_brackets:
            min_b = bracket['min']
            max_b = bracket.get('max')
            rate = bracket['rate']
            taxable_amount = 0
            if state_taxable > min_b:
                if max_b is None:
                    taxable_amount = state_taxable - min_b
                else:
                    taxable_amount = min(state_taxable, max_b) - min_b
                    if taxable_amount < 0:
                        taxable_amount = 0
            tax_due = taxable_amount * rate
            state_tax += tax_due
            if max_b is None or state_taxable > min_b or (min_b == 0 and max_b is not None and max_b > 0):
                state_brackets_result.append({
                    'min': min_b, 'max': max_b, 'rate': rate,
                    'taxableAmount': taxable_amount, 'taxDue': tax_due,
                })
    else:
        state_rate = city.get('stateTaxRate', 0)
        state_tax = state_taxable * state_rate
        if state_rate > 0:
            state_brackets_result.append({
                'min': 0, 'max': None, 'rate': state_rate,
                'taxableAmount': state_taxable, 'taxDue': state_tax,
            })

    # NY child credit
    if country_code == 'US' and num_children_under_17 > 0:
        if city_code in ('NY', 'NYC') or ', NY' in city.get('name', ''):
            threshold = 400000 if is_married else 200000
            excess = max(0, gross_income - threshold)
            reduction = math.ceil(excess / 1000) * 50
            federal_credit_for_state = max(0, num_children_under_17 * 2200 - reduction)
            ny_credit = federal_credit_for_state * 0.33
            if ny_credit > 0:
                credits.append({'name': 'NY State Child Credit', 'amount': ny_credit})
                state_tax = max(0, state_tax - ny_credit)

    local_tax = gross_income * city.get('localTaxRate', 0)
    total_tax = federal_tax + state_tax + local_tax

    return {
        'grossIncome': gross_income,
        'deductions': std_deduction,
        'netTaxableIncome': net_taxable,
        'stateDeductions': state_deduction,
        'stateNetTaxableIncome': state_taxable,
        'brackets': brackets_result,
        'stateBrackets': state_brackets_result,
        'credits': credits,
        'totalTax': total_tax,
        'effectiveRate': total_tax / gross_income if gross_income > 0 else 0,
        'amounts': {'federal': federal_tax, 'state': state_tax, 'local': local_tax},
    }


# ---------------------------------------------------------------------------
# Main calculation
# ---------------------------------------------------------------------------

def calculate_scenario(state: dict, market_data: dict = None, fx_rates: dict = None) -> dict:
    if fx_rates is None:
        fx_rates = {}

    zero_result = {
        'totalAssignmentCost': 0, 'annualAvgCost': 0, 'taxGrossUp': 0, 'hypoTax': 0,
        'hostTaxDetailed': dict(_ZERO_TAX), 'hypoTaxDetailed': dict(_ZERO_TAX),
        'socialSecurity': {'homeEmployee': 0, 'homeEmployer': 0, 'hostEmployee': 0, 'hostEmployer': 0},
        'components': {
            'baseSalary': 0, 'bonus': 0, 'housing': 0, 'schooling': 0, 'cola': 0,
            'transportation': 0, 'homeLeave': 0, 'relocation': 0, 'immigration': 0,
            'taxPreparation': 0, 'utilities': 0,
        },
        'breakdown': [], 'chartBuckets': [],
    }

    home_cc = state.get('homeCountryCode', '')
    host_cc = state.get('hostCountryCode', '')
    if not home_cc or not host_cc:
        return zero_result

    marital_status = state.get('maritalStatus', 'Single')
    num_children_under_17 = state.get('numChildrenUnder17', 0) or 0
    num_children_over_17 = state.get('numChildrenOver17', 0) or 0
    tier_name = state.get('tier', 'Long term assignment')
    is_local_or_plus = tier_name in LOCAL_TIERS
    effective_a1_coc = (
        not is_local_or_plus
        and state.get('hasA1CoC', False)
        and has_totalization_agreement(home_cc, host_cc)
    )

    if not is_local_or_plus and (not state.get('startDate') or not state.get('endDate')):
        return zero_result

    home_city = _get_city(home_cc, state.get('homeCityCode', ''))
    host_city = _get_city(host_cc, state.get('hostCityCode', ''))
    home_country_name = _get_country_name(home_cc)
    host_country_name = _get_country_name(host_cc)
    tier = TIER_BENEFITS.get(tier_name, TIER_BENEFITS['Long term assignment'])

    home_curr = (_get_country(home_cc) or {}).get('currency', 'USD')
    host_curr = (_get_country(host_cc) or {}).get('currency', 'USD')
    input_curr = state.get('currency', 'USD')

    def get_rate(curr):
        return fx_rates.get(curr) or EXCHANGE_RATES.get(curr, 1.0)

    def convert(amount, from_c, to_c):
        if from_c == to_c:
            return amount
        in_usd = amount / get_rate(from_c)
        return in_usd * get_rate(to_c)

    def calc_tax(gross_income, cc, city_code):
        return _calculate_tax_liability(
            gross_income, cc, city_code,
            marital_status, num_children_under_17, num_children_over_17,
        )

    def scale_tax_result(det, from_c, to_c):
        """Re-express a tax detail dict from from_c into to_c."""
        def cv(x):
            return convert(x, from_c, to_c)
        return {
            **det,
            'grossIncome': cv(det['grossIncome']),
            'deductions': cv(det['deductions']),
            'netTaxableIncome': cv(det['netTaxableIncome']),
            'stateDeductions': cv(det.get('stateDeductions', 0)),
            'stateNetTaxableIncome': cv(det.get('stateNetTaxableIncome', 0)),
            'totalTax': cv(det['totalTax']),
            'brackets': [_scale_bracket(b, from_c, to_c, convert) for b in det['brackets']],
            'stateBrackets': [_scale_bracket(b, from_c, to_c, convert) for b in det['stateBrackets']],
            'credits': [{'name': c['name'], 'amount': cv(c['amount'])} for c in det['credits']],
            'amounts': {k: cv(v) for k, v in det['amounts'].items()},
        }

    # Duration
    if is_local_or_plus:
        duration_years = max(1, state.get('durationYears', 1) or 1)
    else:
        from datetime import date
        try:
            start = date.fromisoformat(state['startDate'])
            end = date.fromisoformat(state['endDate'])
        except (KeyError, ValueError):
            return zero_result
        raw = (end - start).days / 365.25
        if raw <= 0:
            return zero_result
        if abs(round(raw) - raw) < 0.01:
            raw = round(raw)
        duration_years = max(0.1, raw)

    # Year portions
    year_portions = []
    remaining = duration_years
    while remaining > 0.001:
        portion = min(1, remaining)
        year_portions.append(portion)
        remaining -= portion

    def build_row(category, amount, description, formula, source, is_one_off=False, source_url=None):
        yearly = []
        for i, portion in enumerate(year_portions):
            if is_one_off:
                yearly.append(amount if i == 0 else 0)
            else:
                yearly.append(amount * portion)
        return {
            'category': category, 'amount': amount, 'yearlyAmounts': yearly,
            'totalAmount': sum(yearly), 'description': description,
            'formula': formula, 'source': source, 'isOneOff': is_one_off,
            'sourceUrl': source_url,
        }

    annual_base = state.get('baseSalary', 0) or 0
    annual_bonus = state.get('bonus', 0) or 0

    # Hypo / base tax
    hypo_tax_annual = 0
    hypo_tax_detailed = dict(_ZERO_TAX)
    host_ss_ee_base = 0

    if is_local_or_plus:
        base_local = convert(annual_base + annual_bonus, input_curr, host_curr)
        base_det_host = calc_tax(base_local, host_cc, state.get('hostCityCode', ''))
        hypo_tax_annual = convert(base_det_host['totalTax'], host_curr, input_curr)
        host_ss_ee_base = convert(calculate_ss(host_cc, base_local, False), host_curr, input_curr)
        hypo_tax_detailed = scale_tax_result(base_det_host, host_curr, input_curr)
    else:
        hypo_income_local = convert(annual_base + annual_bonus, input_curr, home_curr)
        hypo_det_local = calc_tax(hypo_income_local, home_cc, state.get('homeCityCode', ''))
        hypo_tax_annual = convert(hypo_det_local['totalTax'], home_curr, input_curr)
        hypo_tax_detailed = scale_tax_result(hypo_det_local, home_curr, input_curr)

    # Market data overrides
    numbeo_curr = (market_data or {}).get('numbeo', {}).get('currency', host_curr) if market_data else host_curr
    numbeo = (market_data or {}).get('numbeo', {}) if market_data else {}
    sources = (market_data or {}).get('sources', []) if market_data else []
    source_uri = sources[0]['uri'] if sources else None

    total_children = num_children_under_17 + num_children_over_17
    housing_multiplier = 1.0
    family_cat = state.get('familySizeCategory', 'Single')
    if family_cat == 'Couple':
        housing_multiplier = 1.25
    elif family_cat == 'Family':
        housing_multiplier = 1.25 + 0.20 * max(1, total_children)

    # Housing
    housing_base = tier['housingLimit']
    housing_source = 'Mercer 2024 Housing Survey'
    housing_url = 'https://www.mercer.com/solutions/talent-and-transformation/mobility-exchange/housing-data/'
    if numbeo.get('housingMonthly'):
        housing_base = convert(numbeo['housingMonthly'], numbeo_curr, input_curr)
        housing_source = 'Numbeo (Live Market)'
        housing_url = source_uri or housing_url
    housing = (housing_base * housing_multiplier * 12) if state.get('includeHousing') else 0

    # Utilities
    util_base = 250
    util_source = 'Numbeo'
    util_url = 'https://www.numbeo.com/cost-of-living/'
    if numbeo.get('utilitiesMonthly'):
        util_base = convert(numbeo['utilitiesMonthly'], numbeo_curr, input_curr)
        util_source = 'Numbeo (Live Market)'
        util_url = source_uri or util_url
    utilities_allowance = ((util_base * housing_multiplier) * 12) if state.get('includeUtilities') else 0

    # Schooling
    school_base = tier['educationLimit']
    school_source = 'ISC Research'
    school_url = 'https://www.iscresearch.com/'
    if numbeo.get('schoolingAnnual'):
        school_base = convert(numbeo['schoolingAnnual'], numbeo_curr, input_curr)
        school_source = 'Numbeo (Live Market)'
        school_url = source_uri or school_url
    num_school = total_children if total_children > 0 else (1 if state.get('includeSchooling') else 0)
    total_schooling = (school_base * num_school) if state.get('includeSchooling') else 0

    # COLA
    cola_diff = (host_city.get('colaIndex', 100) - home_city.get('colaIndex', 100)) / 100
    cola_allowance = (annual_base * 0.4 * cola_diff) if (state.get('includeCola') and cola_diff > 0) else 0

    transportation = tier['transpLimit'] if state.get('includeTransportation') else 0

    home_leave = 0
    if state.get('includeHomeLeave'):
        family_count = 1
        if family_cat == 'Couple':
            family_count = 2
        elif family_cat == 'Family':
            family_count = 2 + total_children
        home_leave = tier['homeLeaveLimit'] * family_count

    tax_prep = tier['taxPrepLimit'] if state.get('includeTaxPreparation') else 0
    relocation_limit = tier['relocationLimit'] if state.get('includeRelocation') else 0
    immigration_total = tier['immigrationLimit'] if state.get('includeImmigration') else 0

    def calc_host_tax_for_income(income):
        income_local = convert(income, input_curr, host_curr)
        det = calc_tax(income_local, host_cc, state.get('hostCityCode', ''))
        return {
            'total': convert(det['totalTax'], host_curr, input_curr),
            'federal': convert(det['amounts']['federal'], host_curr, input_curr),
            'state': convert(det['amounts']['state'], host_curr, input_curr),
            'local': convert(det['amounts']['local'], host_curr, input_curr),
        }

    def calc_host_ss_for_income(income):
        if effective_a1_coc:
            return {'ee': 0, 'er': 0}
        income_local = convert(income, input_curr, host_curr)
        ee_local = calculate_ss(host_cc, income_local, False)
        er_local = calculate_ss(host_cc, income_local, True)
        return {
            'ee': convert(ee_local, host_curr, input_curr),
            'er': convert(er_local, host_curr, input_curr),
        }

    # Gross-up solver for Local/Plus
    annual_gross_up = 0
    if is_local_or_plus and state.get('includeGrossUp'):
        one_offs_ann = (relocation_limit + immigration_total) / max(1, duration_years)
        net_allowances = (
            housing + total_schooling + cola_allowance + utilities_allowance
            + transportation + home_leave + tax_prep + one_offs_ann
        )
        base_income = annual_base + annual_bonus
        current_gross = net_allowances
        for _ in range(8):
            total_tax_g = calc_host_tax_for_income(base_income + current_gross)['total']
            base_tax_g = calc_host_tax_for_income(base_income)['total']
            marginal_tax = total_tax_g - base_tax_g
            total_ss_g = calc_host_ss_for_income(base_income + current_gross)['ee']
            base_ss_g = calc_host_ss_for_income(base_income)['ee']
            marginal_ss = total_ss_g - base_ss_g
            net_received = current_gross - marginal_tax - marginal_ss
            shortfall = net_allowances - net_received
            if abs(shortfall) < 1:
                break
            current_gross += shortfall
        annual_gross_up = max(0, current_gross - net_allowances)

    # Annual taxable income at host
    def annual_host_taxable_income():
        one_offs_ann = 0
        if is_local_or_plus:
            one_offs_ann = (relocation_limit + immigration_total) / max(1, duration_years)
        if state.get('detachedDutyRelief') and host_cc == 'UK':
            taxable_allowances = total_schooling + tax_prep
        else:
            taxable_allowances = (
                housing + total_schooling + cola_allowance
                + utilities_allowance + transportation + home_leave + tax_prep
            )
        return annual_base + annual_bonus + taxable_allowances + one_offs_ann + (annual_gross_up if is_local_or_plus else 0)

    annual_recurring_host_income = annual_host_taxable_income()
    annual_recurring_local = convert(annual_recurring_host_income, input_curr, host_curr)
    host_det_local = calc_tax(annual_recurring_local, host_cc, state.get('hostCityCode', ''))
    host_tax_detailed = scale_tax_result(host_det_local, host_curr, input_curr)

    host_ss_avg = calc_host_ss_for_income(annual_recurring_host_income)
    host_ss_base_avg = calc_host_ss_for_income(annual_base + annual_bonus) if is_local_or_plus else {'ee': 0, 'er': 0}

    # Yearly relocation (departure + repatriation)
    yearly_relocation = []
    for i in range(len(year_portions)):
        amt = 0
        if state.get('includeRelocation'):
            if i == 0:
                amt += relocation_limit
            if not state.get('excludeRepatriation') and i == len(year_portions) - 1:
                amt += relocation_limit
        yearly_relocation.append(amt)
    total_relocation = sum(yearly_relocation)

    # Yearly host tax
    yearly_host_tax = []
    for i, portion in enumerate(year_portions):
        recurring_tax = calc_host_tax_for_income(annual_recurring_host_income)['total']
        one_offs = 0
        if not state.get('detachedDutyRelief'):
            if i == 0:
                one_offs += immigration_total
            one_offs += yearly_relocation[i]
        total_tax_with_oneoffs = calc_host_tax_for_income(annual_recurring_host_income + one_offs)['total']
        tax_year = (recurring_tax * portion) + (total_tax_with_oneoffs - recurring_tax)
        if is_local_or_plus:
            employee_tax = hypo_tax_annual * portion
            tax_year = max(0, tax_year - employee_tax)
        yearly_host_tax.append(tax_year)

    # Yearly host SS (employer)
    yearly_host_ss_er = []
    for i, portion in enumerate(year_portions):
        recurring_ss = calc_host_ss_for_income(annual_recurring_host_income)['er']
        one_offs = 0
        if not state.get('detachedDutyRelief'):
            if i == 0:
                one_offs += immigration_total
            one_offs += yearly_relocation[i]
        total_ss = calc_host_ss_for_income(annual_recurring_host_income + one_offs)['er']
        yearly_host_ss_er.append((recurring_ss * portion) + (total_ss - recurring_ss))

    # Yearly host SS (employee marginal — Local/Plus only)
    yearly_host_ss_ee_marginal = []
    for i, portion in enumerate(year_portions):
        if not is_local_or_plus:
            yearly_host_ss_ee_marginal.append(0)
            continue
        recurring_ss = calc_host_ss_for_income(annual_recurring_host_income)['ee']
        one_offs = 0
        if not state.get('detachedDutyRelief'):
            if i == 0:
                one_offs += immigration_total
            one_offs += yearly_relocation[i]
        total_ss = calc_host_ss_for_income(annual_recurring_host_income + one_offs)['ee']
        total_ee = (recurring_ss * portion) + (total_ss - recurring_ss)
        base_ee = host_ss_base_avg['ee'] * portion
        yearly_host_ss_ee_marginal.append(max(0, total_ee - base_ee))

    # Home SS
    def calc_home_ss(inc, is_er):
        return calculate_ss(home_cc, inc, is_er)

    full_assignment_income = (
        annual_base + annual_bonus + housing + total_schooling + cola_allowance
        + utilities_allowance + transportation + home_leave + tax_prep
        + (total_relocation + immigration_total) / duration_years
    )
    full_local = convert(full_assignment_income, input_curr, home_curr)
    actual_home_ss_ee = convert(calc_home_ss(full_local, False), home_curr, input_curr)
    actual_home_ss_er = convert(calc_home_ss(full_local, True), home_curr, input_curr)

    if is_local_or_plus:
        hypo_ss_ee_full = host_ss_ee_base
    else:
        base_local_home = convert(annual_base + annual_bonus, input_curr, home_curr)
        hypo_ss_ee_full = convert(calc_home_ss(base_local_home, False), home_curr, input_curr)

    applicable_home_ss_er = actual_home_ss_er if state.get('hasA1CoC') else 0
    applicable_home_ss_ee = actual_home_ss_ee if state.get('hasA1CoC') else 0

    yearly_home_ss_er = [applicable_home_ss_er * p for p in year_portions]
    yearly_home_ss_ee = [applicable_home_ss_ee * p for p in year_portions]
    yearly_hypo_tax = [-hypo_tax_annual * p for p in year_portions]
    yearly_hypo_ss = [-hypo_ss_ee_full * p for p in year_portions]

    # Gross-up per year
    show_hypo = not is_local_or_plus and state.get('includeTaxEqualization')

    yearly_gross_up = []
    for i, host_tax in enumerate(yearly_host_tax):
        if not state.get('includeGrossUp'):
            yearly_gross_up.append(0)
        elif is_local_or_plus:
            yearly_gross_up.append(annual_gross_up * year_portions[i])
        else:
            home_tax = hypo_tax_annual * year_portions[i]
            yearly_gross_up.append(max(0, host_tax - home_tax))

    # Build breakdown
    raw_breakdown = [
        build_row('Base Salary', annual_base, 'Annual Base Salary', 'Fixed Annual', 'Client Input / HRIS'),
        build_row('Annual Bonus', annual_bonus, 'Target Bonus', 'Fixed Annual', 'Client Input / HRIS'),
        {
            'category': 'Hypothetical Tax', 'amount': -hypo_tax_annual if show_hypo else 0,
            'yearlyAmounts': [v if show_hypo else 0 for v in yearly_hypo_tax],
            'totalAmount': sum(yearly_hypo_tax) if show_hypo else 0,
            'description': 'EE Tax Contrib', 'formula': 'Home Rates', 'source': 'Internal',
        },
        {
            'category': 'Hypothetical SS', 'amount': -hypo_ss_ee_full if show_hypo else 0,
            'yearlyAmounts': [v if show_hypo else 0 for v in yearly_hypo_ss],
            'totalAmount': sum(yearly_hypo_ss) if show_hypo else 0,
            'description': 'EE SS Contrib', 'formula': 'Home Rates', 'source': 'Internal',
        },
        build_row('Housing', housing, 'Housing Allowance', 'Market Rate', housing_source, False, housing_url),
        build_row('Education', total_schooling, 'Schooling', 'Market Rate', school_source, False, school_url),
        build_row('Utilities', utilities_allowance, 'Utilities', 'Numbeo', util_source, False, util_url),
        build_row('COLA', cola_allowance, 'COLA', 'Index', 'Mercer 2024 Cost of Living'),
        build_row('Transport', transportation, 'Transport', 'Policy Limit', 'Policy'),
        build_row('Home Leave', home_leave, 'Home Leave', 'Policy Limit', 'Policy'),
        {
            'category': 'Relocation', 'amount': relocation_limit, 'yearlyAmounts': yearly_relocation,
            'totalAmount': total_relocation, 'description': 'Moving', 'isOneOff': True, 'source': 'Policy',
        },
        build_row('Immigration', immigration_total, 'Visa Fees', 'One-off', 'Vendor', True),
        build_row('Tax Services', tax_prep, 'Tax Prep', 'Annual', 'Vendor'),
    ]

    if not is_local_or_plus:
        raw_breakdown.append({
            'category': 'Host Income Tax', 'amount': host_tax_detailed['totalTax'],
            'yearlyAmounts': yearly_host_tax, 'totalAmount': sum(yearly_host_tax),
            'description': f'Host Tax ({host_country_name})', 'formula': 'Host Rules', 'source': 'Internal',
        })
        raw_breakdown.append({
            'category': 'Host SS (EE)', 'amount': 0,
            'yearlyAmounts': yearly_host_ss_ee_marginal, 'totalAmount': 0,
            'description': 'Marginal SS (EE)', 'formula': 'Host Rules', 'source': 'Internal',
        })

    raw_breakdown += [
        {
            'category': 'Host SS (ER)', 'amount': host_ss_avg['er'],
            'yearlyAmounts': yearly_host_ss_er, 'totalAmount': sum(yearly_host_ss_er),
            'description': f'Host SS ({host_country_name})', 'formula': 'Host Rules', 'source': 'Internal',
        },
        {
            'category': 'Home SS (ER)', 'amount': applicable_home_ss_er,
            'yearlyAmounts': yearly_home_ss_er, 'totalAmount': sum(yearly_home_ss_er),
            'description': f'Home SS ({home_country_name})', 'formula': 'Home Rules', 'source': 'Internal',
        },
        {
            'category': 'Home SS (EE)', 'amount': applicable_home_ss_ee,
            'yearlyAmounts': yearly_home_ss_ee, 'totalAmount': sum(yearly_home_ss_ee),
            'description': f'Home SS ({home_country_name})', 'formula': 'Home Rules', 'source': 'Internal',
        },
        {
            'category': 'Gross-up',
            'amount': annual_gross_up if is_local_or_plus else (
                max(0, host_tax_detailed['totalTax'] - hypo_tax_annual) if state.get('includeGrossUp') else 0
            ),
            'yearlyAmounts': yearly_gross_up,
            'totalAmount': (annual_gross_up * duration_years if is_local_or_plus else sum(yearly_gross_up)),
            'description': 'Tax on Tax', 'formula': 'Reconciliation', 'source': 'Internal',
        },
    ]

    # Filter zero rows and add percentage
    breakdown = [
        row for row in raw_breakdown
        if row and abs(row.get('totalAmount', 0)) > 0.01
    ]
    total_cost = sum(r['totalAmount'] for r in breakdown)
    for row in breakdown:
        row['percentage'] = f"{(row['totalAmount'] / total_cost * 100):.1f}" if total_cost > 0 else '0'

    annual_avg = total_cost / duration_years
    total_home_comp = (annual_base + annual_bonus) * duration_years
    total_allowances = (
        (housing + total_schooling + cola_allowance + utilities_allowance
         + transportation + home_leave + tax_prep) * duration_years
        + total_relocation + immigration_total
    )
    total_taxes_ss = (
        sum(yearly_host_tax) + sum(yearly_host_ss_er) + sum(yearly_home_ss_er)
        + sum(yearly_gross_up)
        + (sum(yearly_host_ss_ee_marginal) if is_local_or_plus else 0)
    )

    def pct(v):
        return f"{(v / total_cost * 100):.1f}" if total_cost > 0 else '0'

    chart_buckets = [
        {'name': 'Home Comp', 'value': total_home_comp, 'percentage': pct(total_home_comp)},
        {'name': 'Allowances', 'value': total_allowances, 'percentage': pct(total_allowances)},
        {'name': 'Taxes & SS', 'value': total_taxes_ss, 'percentage': pct(total_taxes_ss)},
    ]

    return {
        'totalAssignmentCost': total_cost,
        'annualAvgCost': annual_avg,
        'taxGrossUp': sum(yearly_gross_up),
        'hypoTax': hypo_tax_annual,
        'hostTaxDetailed': host_tax_detailed,
        'hypoTaxDetailed': hypo_tax_detailed,
        'socialSecurity': {
            'homeEmployee': hypo_ss_ee_full,
            'homeEmployer': 0,
            'hostEmployee': host_ss_avg['ee'],
            'hostEmployer': host_ss_avg['er'],
        },
        'components': {
            'baseSalary': annual_base, 'bonus': annual_bonus, 'housing': housing,
            'schooling': total_schooling, 'cola': cola_allowance, 'transportation': transportation,
            'homeLeave': home_leave, 'relocation': total_relocation, 'immigration': immigration_total,
            'taxPreparation': tax_prep, 'utilities': utilities_allowance,
        },
        'breakdown': breakdown,
        'chartBuckets': chart_buckets,
    }
