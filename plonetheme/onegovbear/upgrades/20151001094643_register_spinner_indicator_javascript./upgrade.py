from ftw.upgrade import UpgradeStep


class RegisterSpinnerIndicatorJavascript(UpgradeStep):
    """Register spinner indicator javascript..
    """

    def __call__(self):
        self.install_upgrade_profile()
