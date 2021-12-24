from django.shortcuts import render, HttpResponseRedirect
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView,CreateView,UpdateView,DeleteView
from .forms import (
    AddressForm,
    RegisteredAddressForm,
    IndividualForm,
    EmailFormSet,
    CompanyForm,
    SharesFormSet,
    TrustForm,
    EditEmailFormSet,
    EditSharesFormSet,
    AddOrEditEventToCheckListForm,
)
from django.urls import reverse_lazy
from .models import (
    Entity, Category, Event, DefaultCheckList, CheckList, 
    InitialResearch, Letter,Inspection,
    Due_Diligence,Property_Serach,MarketResearch,Offer_Finance,Exchange_Settlement,Renovation,ListingForSale,
    Sale_Exchange_Settlement,
)

from django.contrib import messages


class IndividualEntityView(LoginRequiredMixin, View):
    def get_context_data(self, *args, **kwargs):
        ctx = {
            "address_form": AddressForm(),
            "email_formset": EmailFormSet,
            "individual_form": IndividualForm(),
        }
        return ctx

    def get(self, request, *args, **kwargs):
        if Entity.objects.filter(
            user=request.user, entity_type="individual"
        ).exists():
            ctx = {
                "user": Entity.objects.get(
                    user=request.user, entity_type="individual"
                )
            }
            return render(
                request, "settings/entities/individual_entity.html", ctx
            )
        else:
            ctx = self.get_context_data(*args, **kwargs)
            return render(
                request, "settings/entities/individual_entity_form.html", ctx
            )

    def get_success_url(self):
        messages.success(
            self.request,
            "The details have been saved successfully.",
            extra_tags="details_added",
        )
        return reverse_lazy("dashboard:settings:individual_entity")

    def post(self, request, *args, **kwargs):
        address_form = AddressForm(request.POST)
        email_formset = EmailFormSet(request.POST)
        form = IndividualForm(request.POST)
        if (
            form.is_valid()
            and address_form.is_valid()
            and email_formset.is_valid()
        ):
            return self.form_valid(form, email_formset, address_form)
        else:
            return self.form_invalid(form, email_formset, address_form)

    def form_valid(self, form, email_formset, address_form):
        form_object = form.save()
        if address_form.has_changed():
            address_object = address_form.save(commit=False)
            address_object.individual = form_object
            address_object.save()
        for formset_form in email_formset:
            if formset_form.has_changed():
                email_object = formset_form.save(commit=False)
                email_object.individual = form_object
                email_object.save()
        Entity.objects.create(
            user=self.request.user,
            entity_type="individual",
            individual=form_object,
        )
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, email_formset, address_form):
        ctx = {
            "address_form": address_form,
            "email_formset": email_formset,
            "individual_form": form,
        }
        return render(
            self.request, "settings/entities/individual_entity_form.html", ctx
        )


class EditIndividualEntityView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        ctx = self.get_context_data(*args, **kwargs)
        return render(
            request, "settings/entities/individual_entity_form.html", ctx
        )

    def get_context_data(self, *args, **kwargs):
        entity_obj = Entity.objects.select_related("individual").get(
            user=self.request.user, entity_type="individual"
        )
        individual = entity_obj.individual
        ctx = {}
        address_queryset = individual.address_set.all()
        email_queryset = individual.email_set.all()
        if address_queryset:
            address = address_queryset.first()
            ctx["address_form"] = AddressForm(instance=address)
        else:
            ctx["address_form"] = AddressForm()
        if email_queryset:
            ctx["email_formset"] = EditEmailFormSet(queryset=email_queryset)
        else:
            ctx["email_formset"] = EmailFormSet()
        ctx["individual_form"] = IndividualForm(instance=individual)
        return ctx

    def get_success_url(self):
        messages.success(
            self.request,
            "The details have been saved successfully.",
            extra_tags="details_added",
        )
        return reverse_lazy("dashboard:settings:individual_entity")

    def post(self, request, *args, **kwargs):
        entity_object = Entity.objects.select_related(
            "individual__documents"
        ).get(user=self.request.user, entity_type="individual")
        individual = entity_object.individual
        address = None
        email_queryset = individual.email_set.all()
        address_queryset = individual.address_set.all()
        if address_queryset:
            address = address_queryset.first()
        address_form = AddressForm(request.POST, instance=address)
        email_formset = EditEmailFormSet(request.POST, queryset=email_queryset)
        form = IndividualForm(request.POST, instance=individual)
        if (
            form.is_valid()
            and address_form.is_valid()
            and email_formset.is_valid()
        ):
            return self.form_valid(form, email_formset, address_form)
        else:
            return self.form_invalid(form, email_formset, address_form)

    def form_valid(self, form, email_formset, address_form):
        form_object = form.save()
        if address_form.has_changed():
            address_object = address_form.save(commit=False)
            address_object.individual = form_object
            address_object.save()
        email_list = []
        for email in form_object.email_set.all():
            email_list.append(email)
        new_email_list = []
        for formset_form in email_formset:
            email_object = formset_form.save(commit=False)
            email_object.individual = form_object
            email_object.save()
            new_email_list.append(email_object)
        for email in email_list:
            if email not in new_email_list:
                email.delete()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, email_formset, address_form):
        ctx = {
            "address_form": address_form,
            "email_formset": email_formset,
            "individual_form": form,
        }
        return render(
            self.request, "settings/entities/individual_entity_form.html", ctx
        )


class CompanyEntityView(LoginRequiredMixin, View):
    def get_context_data(self, *args, **kwargs):
        ctx = {
            "address_form": AddressForm(prefix="address1"),
            "registered_address_form": RegisteredAddressForm(
                prefix="address2"
            ),
            "email_formset": EmailFormSet,
            "company_form": CompanyForm(),
        }
        return ctx

    def get(self, request, *args, **kwargs):
        if (
            request.path.split("/")[-1] != "add"
            and Entity.objects.filter(
                user=request.user, entity_type="company"
            ).exists()
        ):
            ctx = {
                "entities": Entity.objects.filter(
                    user=request.user, entity_type="company"
                )
            }
            return render(
                request, "settings/entities/company_entity.html", ctx
            )
        else:
            ctx = self.get_context_data(*args, **kwargs)
            return render(
                request, "settings/entities/company_entity_form.html", ctx
            )

    def get_success_url(self):
        messages.success(
            self.request,
            "The details have been saved successfully.",
            extra_tags="details_added",
        )
        return reverse_lazy("dashboard:settings:company_entity")

    def post(self, request, *args, **kwargs):
        address_form = AddressForm(request.POST, prefix="address1")
        registered_address_form = RegisteredAddressForm(
            request.POST, prefix="address2"
        )
        form = CompanyForm(request.POST)
        email_formset = EmailFormSet(request.POST)
        if (
            form.is_valid()
            and address_form.is_valid()
            and registered_address_form.is_valid()
            and email_formset.is_valid()
        ):
            return self.form_valid(
                form, email_formset, address_form, registered_address_form
            )
        else:
            return self.form_invalid(
                form, email_formset, address_form, registered_address_form
            )

    def form_valid(
        self, form, email_formset, address_form, registered_address_form
    ):
        form_object = form.save()
        if address_form.has_changed():
            address_object = address_form.save(commit=False)
            address_object.company = form_object
            address_object.save()
        if registered_address_form.has_changed():
            address_object = registered_address_form.save(commit=False)
            address_object.company = form_object
            address_object.save()
        for formset_form in email_formset:
            if formset_form.has_changed():
                email_object = formset_form.save(commit=False)
                email_object.company = form_object
                email_object.save()
        Entity.objects.create(
            user=self.request.user, entity_type="company", company=form_object
        )
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(
        self, form, email_formset, address_form, registered_address_form
    ):
        ctx = {
            "address_form": address_form,
            "registered_address_form": registered_address_form,
            "email_formset": email_formset,
            "company_form": form,
        }
        return render(
            self.request, "settings/entities/company_entity_form.html", ctx
        )


class EditCompanyEntityView(LoginRequiredMixin, View):
    def get_context_data(self, *args, **kwargs):
        entity_obj = Entity.objects.select_related("company").get(
            pk=self.kwargs["pk"]
        )
        company = entity_obj.company
        address = registered_address = None
        ctx = {}
        email_queryset = company.email_set.all()
        address_queryset = company.address_set.all()
        registered_address_queryset = company.registeredaddress_set.all()
        if address_queryset:
            address = company.address_set.first()
        ctx["address_form"] = AddressForm(instance=address, prefix="address1")
        if registered_address_queryset:
            registered_address = registered_address_queryset.first()
        ctx["registered_address_form"] = AddressForm(
            instance=registered_address, prefix="address2"
        )
        if email_queryset:
            ctx["email_formset"] = EditEmailFormSet(queryset=email_queryset)
        else:
            ctx["email_formset"] = EmailFormSet()
        ctx["company_form"] = CompanyForm(instance=company)
        return ctx

    def get(self, request, *args, **kwargs):
        ctx = self.get_context_data(*args, **kwargs)
        return render(
            request, "settings/entities/company_entity_form.html", ctx
        )

    def get_success_url(self):
        messages.success(
            self.request,
            "The details have been saved successfully.",
            extra_tags="details_added",
        )
        return reverse_lazy("dashboard:settings:company_entity")

    def post(self, request, *args, **kwargs):
        entity_obj = Entity.objects.select_related("company").get(
            pk=self.kwargs["pk"]
        )
        company = entity_obj.company
        address = registered_address = None
        email_queryset = company.email_set.all()
        address_queryset = company.address_set.all()
        registered_address_queryset = company.registeredaddress_set.all()
        if address_queryset:
            address = address_queryset.first()
        if registered_address_queryset:
            registered_address = registered_address_queryset.first()
        address_form = AddressForm(
            request.POST, instance=address, prefix="address1"
        )
        registered_address_form = RegisteredAddressForm(
            request.POST, instance=registered_address, prefix="address2"
        )
        email_formset = EditEmailFormSet(request.POST, queryset=email_queryset)
        form = CompanyForm(request.POST, instance=company)
        if (
            form.is_valid()
            and address_form.is_valid()
            and registered_address_form.is_valid()
            and email_formset.is_valid()
        ):
            return self.form_valid(
                form, email_formset, address_form, registered_address_form
            )
        else:
            return self.form_invalid(
                form, email_formset, address_form, registered_address_form
            )

    def form_valid(
        self, form, email_formset, address_form, registered_address_form
    ):
        form_object = form.save()
        if address_form.has_changed():
            address_object = address_form.save(commit=False)
            address_object.company = form_object
            address_object.save()
        if registered_address_form.has_changed():
            address_object = registered_address_form.save(commit=False)
            address_object.company = form_object
            address_object.save()
        email_list = []
        for email in form_object.email_set.all():
            email_list.append(email)
        new_email_list = []
        for formset_form in email_formset:
            email_object = formset_form.save(commit=False)
            email_object.company = form_object
            email_object.save()
            new_email_list.append(email_object)
        for email in email_list:
            if email not in new_email_list:
                email.delete()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(
        self, form, email_formset, address_form, registered_address_form
    ):
        ctx = {
            "address_form": address_form,
            "registered_address_form": registered_address_form,
            "email_formset": email_formset,
            "company_form": form,
        }
        return render(
            self.request, "settings/entities/company_entity_form.html", ctx
        )


class TrustEntityView(LoginRequiredMixin, View):
    def get_context_data(self, *args, **kwargs):
        ctx = {
            "email_formset": EmailFormSet(prefix="email_formset"),
            "shares_formset": SharesFormSet(prefix="shares_formset"),
            "trust_form": TrustForm(),
        }
        return ctx

    def get(self, request, *args, **kwargs):
        if (
            request.path.split("/")[-1] != "add"
            and Entity.objects.filter(
                user=request.user, entity_type="trust"
            ).exists()
        ):
            ctx = {
                "entities": Entity.objects.filter(
                    user=request.user, entity_type="trust"
                )
            }
            return render(request, "settings/entities/trust_entity.html", ctx)
        else:
            ctx = self.get_context_data(*args, **kwargs)
            return render(
                request, "settings/entities/trust_entity_form.html", ctx
            )

    def get_success_url(self):
        messages.success(
            self.request,
            "The details have been saved successfully.",
            extra_tags="details_added",
        )
        return reverse_lazy("dashboard:settings:trust_entity")

    def post(self, request, *args, **kwargs):
        form = TrustForm(request.POST)
        email_formset = EmailFormSet(request.POST, prefix="email_formset")
        shares_formset = SharesFormSet(request.POST, prefix="shares_formset")
        if (
            form.is_valid()
            and email_formset.is_valid()
            and shares_formset.is_valid()
        ):
            return self.form_valid(form, email_formset, shares_formset)
        else:
            return self.form_invalid(form, email_formset, shares_formset)

    def form_valid(self, form, email_formset, shares_formset):
        form_object = form.save()
        for formset_form in email_formset:
            if formset_form.has_changed():
                email_object = formset_form.save(commit=False)
                email_object.trust = form_object
                email_object.save()
        for formset_form in shares_formset:
            if formset_form.cleaned_data.get("name", None):
                share_object = formset_form.save(commit=False)
                share_object.trust = form_object
                share_object.save()
        Entity.objects.create(
            user=self.request.user, entity_type="trust", trust=form_object
        )
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(
        self, form, email_formset, shares_formset, documents_form
    ):
        ctx = {
            "email_formset": email_formset,
            "shares_formset": shares_formset,
            "trust_form": form,
        }
        return render(
            self.request, "settings/entities/trust_entity_form.html", ctx
        )


class EditTrustEntityView(LoginRequiredMixin, View):
    def get_context_data(self, *args, **kwargs):
        entity_obj = Entity.objects.select_related("trust").get(
            pk=self.kwargs["pk"]
        )
        trust = entity_obj.trust
        ctx = {}
        email_queryset = trust.email_set.all()
        shares_queryset = trust.shares_set.all()
        if email_queryset:
            ctx["email_formset"] = EditEmailFormSet(
                queryset=email_queryset, prefix="email_formset"
            )
        else:
            ctx["email_formset"] = EmailFormSet(prefix="email_formset")
        if shares_queryset:
            ctx["shares_formset"] = EditSharesFormSet(
                queryset=shares_queryset, prefix="shares_formset"
            )
        else:
            ctx["shares_formset"] = SharesFormSet(prefix="shares_formset")
        ctx["trust_form"] = TrustForm(instance=trust)
        return ctx

    def get(self, request, *args, **kwargs):
        ctx = self.get_context_data(*args, **kwargs)
        return render(request, "settings/entities/trust_entity_form.html", ctx)

    def get_success_url(self):
        messages.success(
            self.request,
            "The details have been saved successfully.",
            extra_tags="details_added",
        )
        return reverse_lazy("dashboard:settings:trust_entity")

    def post(self, request, *args, **kwargs):
        entity_obj = Entity.objects.select_related("trust").get(
            pk=self.kwargs["pk"]
        )
        trust = entity_obj.trust
        email_queryset = trust.email_set.all()
        shares_queryset = trust.shares_set.all()
        email_formset = EditEmailFormSet(
            request.POST, queryset=email_queryset, prefix="email_formset"
        )
        shares_formset = EditSharesFormSet(
            request.POST, queryset=shares_queryset, prefix="shares_formset"
        )
        form = TrustForm(request.POST, instance=trust)
        if (
            form.is_valid()
            and email_formset.is_valid()
            and shares_formset.is_valid()
        ):
            return self.form_valid(form, email_formset, shares_formset)
        else:
            return self.form_invalid(form, email_formset, shares_formset)

    def form_valid(self, form, email_formset, shares_formset):
        form_object = form.save()
        emails_list = []
        for email in form_object.email_set.all():
            emails_list.append(email)
        new_emails_list = []
        for formset_form in email_formset:
            email_object = formset_form.save(commit=False)
            email_object.trust = form_object
            email_object.save()
            new_emails_list.append(email_object)
        for email in emails_list:
            if email not in new_emails_list:
                email.delete()

        shares_list = []
        for share in form_object.shares_set.all():
            shares_list.append(share)
        new_shares_list = []
        for formset_form in shares_formset:
            if formset_form.cleaned_data.get("name", None):
                share_object = formset_form.save(commit=False)
                share_object.trust = form_object
                share_object.save()
                new_shares_list.append(share_object)
        for share in shares_list:
            if share not in new_shares_list:
                share.delete()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, email_formset, shares_formset):
        ctx = {
            "email_formset": email_formset,
            "shares_formset": shares_formset,
            "trust_form": form,
        }
        return render(
            self.request, "settings/entities/trust_entity_form.html", ctx
        )


class CheckListView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        ctx = self.get_context_data(*args, **kwargs)
        return render(request, "settings/checklist/checklist.html", ctx)

    def get_context_data(self, *args, **kwargs):
        checklist_objects = DefaultCheckList.objects.filter(
            user=self.request.user,
            category__category_name=kwargs["checklist_category"],
        )
        ctx = {
            "checklist_objects": checklist_objects,
            "checklist_category": kwargs["checklist_category"],
        }
        return ctx
        

class AddEventToCheckListView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        ctx = {"form": AddOrEditEventToCheckListForm, "add_or_edit": "add"}
        return render(
            request, "settings/checklist/add_or_edit_event_checklist.html", ctx
        )

    def get_success_url(self):
        messages.success(
            self.request,
            "The event have been saved successfully",
            extra_tags="details_updated",
        )
        return reverse_lazy(
            "dashboard:settings:checklist",
            kwargs={"checklist_category": self.kwargs["checklist_category"]},
        )

    def post(self, request, *args, **kwargs):
        form = AddOrEditEventToCheckListForm(request.POST)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        event=form.cleaned_data['event_name']
        print(event)
        form_object = form.save(commit=False)
        # Get event object with the new event name
        event_objects = Event.objects.filter(event_name=event)
        try:
            category_object = Category.objects.get(
            category_name=self.kwargs["checklist_category"])
            
        
        except Category.DoesNotExist:
            category_object=None
        
        # If event object exists with the new event name, create a new checklist and assign it to the defaultchecklist
        if event_objects or category_object:
            checklist_objects = DefaultCheckList.objects.filter(
                user=self.request.user, event=event_objects.first()
            )
            if not checklist_objects:
                DefaultCheckList.objects.create(
                    user=self.request.user,
                    category=category_object,
                    event=event_objects.first(),
                )
                # Get all unique deal ids for creating new checklist objects
                deal_ids = (
                    CheckList.objects.filter(user=self.request.user)
                    .values("deal")
                    .distinct()
                )
                # For each deal, create a checklist object
                for deal in deal_ids:
                    CheckList.objects.create(
                        user=self.request.user,
                        deal_id=deal["deal"],
                        category=category_object,
                        event=event_objects.first(),
                    )
        # Else, create a new event, create a new checklist and assign the new event to defaultchecklist
        else:
            form_object.save()
            DefaultCheckList.objects.create(
                user=self.request.user,
                category=category_object,
                event=form_object,
            )
            # Get all unique deal ids for creating new checklist objects
            deal_ids = (
                CheckList.objects.filter(user=self.request.user)
                .values("deal")
                .distinct()
            )
            # For each deal, create a checklist object
            for deal in deal_ids:
                CheckList.objects.create(
                    user=self.request.user,
                    deal_id=deal["deal"],
                    category=category_object,
                    event=form_object,
                )
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        ctx = {"form": form, "add_or_edit": "add"}
        return render(
            self.request,
            "settings/checklist/add_or_edit_event_checklist.html",
            ctx,
        )


class EditEventOfCheckListView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        default_checklist_object = DefaultCheckList.objects.select_related(
            "event"
        ).get(pk=kwargs["pk"])
        ctx = {
            "form": AddOrEditEventToCheckListForm(
                initial={
                    "event_name": default_checklist_object.event.event_name
                }
            ),
            "add_or_edit": "edit",
        }
        return render(
            request, "settings/checklist/add_or_edit_event_checklist.html", ctx
        )

    def get_success_url(self):
        messages.success(
            self.request,
            "The event have been saved successfully",
            extra_tags="details_updated",
        )
        return reverse_lazy(
            "dashboard:settings:checklist",
            kwargs={"checklist_category": self.kwargs["checklist_category"]},
        )

    def post(self, request, *args, **kwargs):
        form = AddOrEditEventToCheckListForm(request.POST)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form_object = form.save(commit=False)
        # CheckList object
        default_checklist_object = DefaultCheckList.objects.select_related(
            "event"
        ).get(pk=self.kwargs["pk"])
        # Check how many checklist objects exist having the old event
        default_checklist_objects = DefaultCheckList.objects.filter(
            event=default_checklist_object.event
        )
        # If one checklist object exists with the existing event
        if len(default_checklist_objects) == 1:
            # Get event objects with the new event
            event_objects = Event.objects.filter(
                event_name=form_object.event_name
            )
            # If event objects exist with the new event, then the previous event will be deleted and a new event will be created and assigned to checklist
            if event_objects:
                default_checklist_objects_with_new_event = DefaultCheckList.objects.filter(
                    user=self.request.user, event=event_objects[0]
                )
                if default_checklist_objects_with_new_event:
                    CheckList.objects.filter(
                        user=self.request.user,
                        event=default_checklist_object.event,
                    ).delete()
                    default_checklist_object.delete()
                else:
                    event_object = default_checklist_object.event
                    default_checklist_object.event = event_objects[0]
                    default_checklist_object.save()
                    # Edit all checklist objects as well
                    checklist_objects = CheckList.objects.select_related(
                        "event"
                    ).filter(user=self.request.user, event=event_object)
                    for checklist_object in checklist_objects:
                        checklist_object.event = event_objects[0]
                        checklist_object.save()
                    if event_object.default_event is False:
                        event_object.delete()
            # Else, the event with new event name will be assigned to the checklist
            else:
                event_object = default_checklist_object.event
                event_object.event_name = form_object.event_name
                event_object.save()
        # If more than one checklist objects exist with the event
        else:
            # Get all checklist objects with the new event name
            event_objects = Event.objects.filter(
                event_name=form_object.event_name
            )
            # If objects exist with the new event name, then assign them to the checklist object
            if event_objects:
                default_checklist_objects_with_new_event = DefaultCheckList.objects.filter(
                    user=self.request.user, event=event_objects[0]
                )
                if default_checklist_objects_with_new_event:
                    CheckList.objects.filter(
                        user=self.request.user,
                        event=default_checklist_object.event,
                    ).delete()
                    default_checklist_object.delete()
                else:
                    event_object = Event.objects.get(
                        event_name=form_object.event_name
                    )
                    default_checklist_object.event = event_object
                    default_checklist_object.save()

                    previous_event_object = default_checklist_object.event
                    # Edit all checklist objects as well
                    checklist_objects = CheckList.objects.filter(
                        user=self.request.user, event=previous_event_object
                    )
                    for checklist_object in checklist_objects:
                        checklist_object.event = event_object
                        checklist_object.save()
            # Else create a new event with the new event name and assign it to the checklist object
            else:
                form_object.save()
                default_checklist_object.event = form_object
                default_checklist_object.save()
                event_object = default_checklist_object.event
                # Edit all checklist objects as well
                checklist_objects = CheckList.objects.filter(
                    user=self.request.user, event=event_object
                )
                for checklist_object in checklist_objects:
                    checklist_object.event = form_object
                    checklist_object.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        ctx = {"form": form, "add_or_edit": "edit"}
        return render(
            self.request,
            "settings/checklist/add_or_edit_event_checklist.html",
            ctx,
        )


class DeleteEventOfCheckListView(View):

    """
    View to delete a checklist and/or event for a user
    """

    def get_success_url(self):
        messages.success(
            self.request,
            "The event have been deleted successfully",
            extra_tags="details_updated",
        )
        return reverse_lazy(
            "dashboard:settings:checklist",
            kwargs={"checklist_category": self.kwargs["checklist_category"]},
        )

    def get(self, request, *args, **kwargs):
        default_checklist_object = DefaultCheckList.objects.select_related(
            "category", "event"
        ).get(pk=self.kwargs["pk"])
        # Delete all checklist objects corresponding to the above default checklist object
        CheckList.objects.filter(
            user=self.request.user,
            category=default_checklist_object.category,
            event=default_checklist_object.event,
        ).delete()
        default_checklist_objects = DefaultCheckList.objects.filter(
            event=default_checklist_object.event
        )
        if len(default_checklist_objects) == 1:
            event_object = default_checklist_object.event
            if event_object.default_event is False:
                event_object.delete()
        default_checklist_object.delete()
        return HttpResponseRedirect(self.get_success_url())
 
#Initial Reasearch View
class InitialListView(LoginRequiredMixin,ListView):
    model=InitialResearch
    
class InitialCreateView(LoginRequiredMixin,CreateView):
    model=InitialResearch    
    fields='__all__'
    
class InitialUpdateView(LoginRequiredMixin,UpdateView):
    model=InitialResearch    
    fields='__all__'   
          
class InitialDeleteView(LoginRequiredMixin,DeleteView):
    model=InitialResearch
    fields = '__all__'
    success_url=reverse_lazy('dashboard:settings:initial-list') 

#Letter View
class LetterListView(LoginRequiredMixin,ListView):
    model=Letter
    
class LetterCreateView(LoginRequiredMixin,CreateView):
    model=Letter
    fields = '__all__'
     
    
class LetterUpdateView(LoginRequiredMixin,UpdateView):
    model=Letter
    fields = '__all__'
    
    
class LetterDeleteView(LoginRequiredMixin,DeleteView):
    model=Letter
    fields = '__all__'
    success_url=reverse_lazy('dashboard:settings:letter-list') 
    
#inspection
class InspectionListView(LoginRequiredMixin,ListView):
    model=Inspection
    
class InspectionCreateView(LoginRequiredMixin,CreateView):
    model=Inspection
    fields = '__all__'
     
    
class InspectionUpdateView(LoginRequiredMixin,UpdateView):
    model=Inspection
    fields = '__all__'
    
    
class InspectionDeleteView(LoginRequiredMixin,DeleteView):
    model=Inspection
    fields = '__all__'
    success_url=reverse_lazy('dashboard:settings:inspection-list')
    
#Due_dilligence
class Due_DiligenceListView(LoginRequiredMixin,ListView):
    model=Due_Diligence
    
class Due_DiligenceCreateView(LoginRequiredMixin,CreateView):
    model=Due_Diligence
    fields = '__all__'
     
    
class Due_DiligenceUpdateView(LoginRequiredMixin,UpdateView):
    model=Due_Diligence
    fields = '__all__'
    
    
class Due_DiligenceDeleteView(LoginRequiredMixin,DeleteView):
    model=Due_Diligence
    fields = '__all__'
    success_url=reverse_lazy('dashboard:settings:duedilligence-list') 
    
#PropertySerach
class Property_SerachListView(LoginRequiredMixin,ListView):
    model=Property_Serach
    
class Property_SerachCreateView(LoginRequiredMixin,CreateView):
    model=Property_Serach
    fields = '__all__'
     
    
class Property_SerachUpdateView(LoginRequiredMixin,UpdateView):
    model=Property_Serach
    fields = '__all__'
    
    
class Property_SerachDeleteView(LoginRequiredMixin,DeleteView):
    model=Property_Serach
    fields = '__all__'
    success_url=reverse_lazy('dashboard:settings:propertysearch-list')
    
#MarketResearch
class MarketResearchListView(LoginRequiredMixin,ListView):
    model=MarketResearch
    
class MarketResearchCreateView(LoginRequiredMixin,CreateView):
    model=MarketResearch
    fields = '__all__'
     
    
class MarketResearchUpdateView(LoginRequiredMixin,UpdateView):
    model=MarketResearch
    fields = '__all__'
    
    
class MarketResearchDeleteView(LoginRequiredMixin,DeleteView):
    model=MarketResearch
    fields = '__all__'
    success_url=reverse_lazy('dashboard:settings:marketresearch-list')
    
#Offer/Finance
class Offer_FinanceListView(LoginRequiredMixin,ListView):
    model=Offer_Finance
    
class Offer_FinanceCreateView(LoginRequiredMixin,CreateView):
    model=Offer_Finance
    fields = '__all__'
     
    
class Offer_FinanceUpdateView(LoginRequiredMixin,UpdateView):
    model=Offer_Finance
    fields = '__all__'
    
    
class Offer_FinanceDeleteView(LoginRequiredMixin,DeleteView):
    model=Offer_Finance
    fields = '__all__'
    success_url=reverse_lazy('dashboard:settings:offerfinance-list')
    
#Exchange/Settlement
class Exchange_SettlementListView(LoginRequiredMixin,ListView):
    model=Exchange_Settlement
    
class Exchange_SettlementCreateView(LoginRequiredMixin,CreateView):
    model=Exchange_Settlement
    fields = '__all__'
     
    
class Exchange_SettlementUpdateView(LoginRequiredMixin,UpdateView):
    model=Exchange_Settlement
    fields = '__all__'
    
    
class Exchange_SettlementDeleteView(LoginRequiredMixin,DeleteView):
    model=Exchange_Settlement
    fields = '__all__'
    success_url=reverse_lazy('dashboard:settings:exchangesettlement-list')
    
#Renovation
class RenovationListView(LoginRequiredMixin,ListView):
    model=Renovation
    
class RenovationCreateView(LoginRequiredMixin,CreateView):
    model=Renovation
    fields = '__all__'
     
    
class RenovationUpdateView(LoginRequiredMixin,UpdateView):
    model=Renovation
    fields = '__all__'
    
    
class RenovationDeleteView(LoginRequiredMixin,DeleteView):
    model=Renovation
    fields = '__all__'
    success_url=reverse_lazy('dashboard:settings:renovation-list')
    
#ListingForSale
class ListingForSaleListView(LoginRequiredMixin,ListView):
    model=ListingForSale
    
class ListingForSaleCreateView(LoginRequiredMixin,CreateView):
    model=ListingForSale
    fields = '__all__'
     
    
class ListingForSaleUpdateView(LoginRequiredMixin,UpdateView):
    model=ListingForSale
    fields = '__all__'
    
    
class ListingForSaleDeleteView(LoginRequiredMixin,DeleteView):
    model=ListingForSale
    fields = '__all__'
    success_url=reverse_lazy('dashboard:settings:listingforsale-list')
    
#Sale_Exchange_Settlement
class Sale_Exchange_SettlementListView(LoginRequiredMixin,ListView):
    model=Sale_Exchange_Settlement
    
class Sale_Exchange_SettlementCreateView(LoginRequiredMixin,CreateView):
    model=Sale_Exchange_Settlement
    fields = '__all__'
     
    
class Sale_Exchange_SettlementUpdateView(LoginRequiredMixin,UpdateView):
    model=Sale_Exchange_Settlement
    fields = '__all__'
    
    
class Sale_Exchange_SettlementDeleteView(LoginRequiredMixin,DeleteView):
    model=Sale_Exchange_Settlement
    fields = '__all__'
    success_url=reverse_lazy('dashboard:settings:saleexchangesettlement-list')
    
    

    

    

    