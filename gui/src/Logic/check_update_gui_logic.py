from src.IMainManagerAdapter import IMainManagerAdapter
from src.ILogic import ILogic, LogicResult


class CheckUpdateGuiLogic(ILogic):
    def __init__(self, main_manager):
        self.main_manager = main_manager

    def execute(self, repo_owner, repo_name):
        result = self.main_manager.get_network_manager().check_server_status()
        if result is None:
            return LogicResult(False, error="GUI server is down")

        return LogicResult(True, value=False)
