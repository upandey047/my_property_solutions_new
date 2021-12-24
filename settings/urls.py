from django.urls import path
from . import views

app_name = "settings"

urlpatterns = [
    # path('initialresearch1/',views.initial_research,name='init'),
    
    
    
    
    path("initial-research/",views.InitialListView.as_view(),name="initial-list",),
    path("initial-research-add/",views.InitialCreateView.as_view(),name="initial-create",),
    path("initial-research-update/<int:pk>",views.InitialUpdateView.as_view(),name="initial-update",),
    path("initial-research-delete/<int:pk>",views.InitialDeleteView.as_view(),name="initial-delete",),
    path("letter/",views.LetterListView.as_view(),name="letter-list",),
    path("letter-add/",views.LetterCreateView.as_view(),name="letter-create",),
    path("letter-update/<int:pk>",views.LetterUpdateView.as_view(),name="letter-update",),
    path("letter-delete/<int:pk>",views.LetterDeleteView.as_view(),name="letter-delete",),
    path("inspection/",views.InspectionListView.as_view(),name="inspection-list",),
    path("inspection-add/",views.InspectionCreateView.as_view(),name="inspection-create",),
    path("inspection-update/<int:pk>",views.InspectionUpdateView.as_view(),name="inspection-update",),
    path("inspection-delete/<int:pk>",views.InspectionDeleteView.as_view(),name="inspection-delete",),
    path("duedilligence/",views.Due_DiligenceListView.as_view(),name="duedilligence-list",),
    path("duedilligence-add/",views.Due_DiligenceCreateView.as_view(),name="duedilligence-create",),
    path("duedilligence-update/<int:pk>",views.Due_DiligenceUpdateView.as_view(),name="duedilligence-update",),
    path("duedilligence-delete/<int:pk>",views.Due_DiligenceDeleteView.as_view(),name="duedilligence-delete",),
    path("propertyserach/",views.Property_SerachListView.as_view(),name="propertysearch-list",),
    path("propertyserach-add/",views.Property_SerachCreateView.as_view(),name="propertysearch-create",),
    path("propertyserach-update/<int:pk>",views.Property_SerachUpdateView.as_view(),name="propertysearch-update",),
    path("propertyserach-delete/<int:pk>",views.Property_SerachDeleteView.as_view(),name="propertysearch-delete",),
    path("marketresearch/",views.MarketResearchListView.as_view(),name="marketresearch-list",),
    path("marketresearch-add/",views.MarketResearchCreateView.as_view(),name="marketresearch-create",),
    path("marketresearch-update/<int:pk>",views.MarketResearchUpdateView.as_view(),name="marketresearch-update",),
    path("marketresearch-delete/<int:pk>",views.MarketResearchDeleteView.as_view(),name="marketresearch-delete",),
    path("offerfinance/",views.Offer_FinanceListView.as_view(),name="offerfinance-list",),
    path("offerfinance-add/",views.Offer_FinanceCreateView.as_view(),name="offerfinance-create",),
    path("offerfinance-update/<int:pk>",views.Offer_FinanceUpdateView.as_view(),name="offerfinance-update",),
    path("offerfinance-delete/<int:pk>",views.Offer_FinanceDeleteView.as_view(),name="offerfinance-delete",),
    path("exchangesettlement/",views.Exchange_SettlementListView.as_view(),name="exchangesettlement-list",),
    path("exchangesettlement-add/",views.Exchange_SettlementCreateView.as_view(),name="exchangesettlement-create",),
    path("exchangesettlement-update/<int:pk>",views.Exchange_SettlementUpdateView.as_view(),name="exchangesettlement-update",),
    path("exchangesettlement-delete/<int:pk>",views.Exchange_SettlementDeleteView.as_view(),name="exchangesettlement-delete",),
    path("renovation/",views.RenovationListView.as_view(),name="renovation-list",),
    path("renovation-add/",views.RenovationCreateView.as_view(),name="renovation-create",),
    path("renovation-update/<int:pk>",views.RenovationUpdateView.as_view(),name="renovation-update",),
    path("renovation-delete/<int:pk>",views.RenovationDeleteView.as_view(),name="renovation-delete",),
    path("listingforsale/",views.ListingForSaleListView.as_view(),name="listingforsale-list",),
    path("listingforsale-add/",views.ListingForSaleCreateView.as_view(),name="listingforsale-create",),
    path("listingforsale-update/<int:pk>",views.ListingForSaleUpdateView.as_view(),name="listingforsale-update",),
    path("listingforsale-delete/<int:pk>",views.ListingForSaleDeleteView.as_view(),name="listingforsale-delete",),
    path("saleexchangesettlement/",views.Sale_Exchange_SettlementListView.as_view(),name="saleexchangesettlement-list",),
    path("saleexchangesettlement-add/",views.Sale_Exchange_SettlementCreateView.as_view(),name="saleexchangesettlement-create",),
    path("saleexchangesettlement-update/<int:pk>",views.Sale_Exchange_SettlementUpdateView.as_view(),name="saleexchangesettlement-update",),
    path("saleexchangesettlement-delete/<int:pk>",views.Sale_Exchange_SettlementDeleteView.as_view(),name="saleexchangesettlement-delete",),
    path(
        "individual",
        views.IndividualEntityView.as_view(),
        name="individual_entity",
    ),
    path("company", views.CompanyEntityView.as_view(), name="company_entity"),
    path("trust", views.TrustEntityView.as_view(), name="trust_entity"),
    path(
        "individual/edit/<int:pk>",
        views.EditIndividualEntityView.as_view(),
        name="edit_individual_entity",
    ),
    path(
        "company/edit/<int:pk>",
        views.EditCompanyEntityView.as_view(),
        name="edit_company_entity",
    ),
    path(
        "trust/edit/<int:pk>",
        views.EditTrustEntityView.as_view(),
        name="edit_trust_entity",
    ),
    path(
        "individual/add",
        views.IndividualEntityView.as_view(),
        name="add_individual_entity",
    ),
    path(
        "company/add",
        views.CompanyEntityView.as_view(),
        name="add_company_entity",
    ),
    path(
        "trust/add", views.TrustEntityView.as_view(), name="add_trust_entity"
    ),
    path(
        "checklist/<slug:checklist_category>",
        views.CheckListView.as_view(),
        name="checklist",
    ),
    path(
        "checklist/<slug:checklist_category>/add",
        views.AddEventToCheckListView.as_view(),
        name="add_event_to_checklist",
    ),
    path(
        "checklist/<slug:checklist_category>/edit/<int:pk>",
        views.EditEventOfCheckListView.as_view(),
        name="edit_event_of_checklist",
    ),
    path(
        "checklist/<slug:checklist_category>/delete/<int:pk>",
        views.DeleteEventOfCheckListView.as_view(),
        name="delete_event_of_checklist",
    ),
]
