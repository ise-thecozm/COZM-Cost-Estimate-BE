from django.urls import path
from api.views import auth, state, estimates, market, fx, calculate, reference, export

urlpatterns = [
    # Auth
    path('auth/login', auth.login),
    path('auth/logout', auth.logout),
    path('auth/verify', auth.verify),

    # Mobility state — GET and PUT on same path, handled by method dispatch in view
    path('state', state.state_view),

    # Estimates
    path('estimates', estimates.estimates_list_create),
    path('estimates/<uuid:pk>', estimates.estimate_detail),
    path('estimates/<uuid:pk>/similar', estimates.similar_estimates),

    # Market
    path('market/insight', market.market_insight),

    # FX
    path('fx/rates', fx.fx_rates),

    # Calculation
    path('calculate', calculate.calculate),

    # Reference data
    path('locations', reference.locations),
    path('tiers', reference.tiers),
    path('country-insights/<str:code>', reference.country_insight),
    path('totalization-agreements', reference.totalization_agreements),

    # Export
    path('export/pdf', export.export_pdf),
    path('export/excel', export.export_excel),
]
