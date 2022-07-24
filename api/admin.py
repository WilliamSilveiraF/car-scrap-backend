from django.contrib import admin

import api.models as model


admin.site.register(model.Company)
admin.site.register(model.Order)