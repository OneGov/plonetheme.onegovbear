from ftw.upgrade import UpgradeStep


class DefinePathbarFullWidthVariableInRegisty(UpgradeStep):
    """Define pathbar full width variable in registy.xml.
    """

    def __call__(self):
        self.install_upgrade_profile()
