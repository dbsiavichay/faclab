class SiteFormMixin:
    def get_initial(self):
        if self.object:
            return self.object.sri_config
