from django.contrib import admin
from .models import (
    Address,
    RegisteredAddress,
    Email,
    Documents,
    Individual,
    Company,
    Shares,
    Trust,
    Entity,
    Category,
    Event,
    CheckList,
    DefaultCheckList,
    Entity, Category, Event, 
  DefaultCheckList, CheckList,
  InitialResearch, Letter,Inspection,
  Due_Diligence,Property_Serach,MarketResearch,Offer_Finance,Exchange_Settlement,Renovation,ListingForSale,
  Sale_Exchange_Settlement,
)

admin.site.register(InitialResearch)
admin.site.register(Inspection)
admin.site.register(Due_Diligence)
admin.site.register(Property_Serach)
admin.site.register(Letter)
admin.site.register(MarketResearch)
admin.site.register(Offer_Finance)
admin.site.register(Exchange_Settlement)
admin.site.register(Renovation)
admin.site.register(ListingForSale)
admin.site.register(Sale_Exchange_Settlement)
admin.site.register(Address)
admin.site.register(RegisteredAddress)
admin.site.register(Email)
admin.site.register(Documents)
admin.site.register(Individual)
admin.site.register(Company)
admin.site.register(Shares)
admin.site.register(Trust)
admin.site.register(Entity)
admin.site.register(Category)
admin.site.register(Event)
admin.site.register(CheckList)
admin.site.register(DefaultCheckList)
