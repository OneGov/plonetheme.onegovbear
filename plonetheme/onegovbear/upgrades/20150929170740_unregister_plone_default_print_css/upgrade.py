from ftw.upgrade import UpgradeStep


class PloneDefaultPrintCSS(UpgradeStep):
    """Replace plone default print.css with custom one based on ftw.theming.
    """

    def __call__(self):
        self.install_upgrade_profile()