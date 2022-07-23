from django.contrib import admin

import polls.models as model


admin.site.register(model.Company)
admin.site.register(model.Order)