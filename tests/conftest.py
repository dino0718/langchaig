import pytest
import sys
import os

# 將專案根目錄加入 Python 路徑
@pytest.fixture(autouse=True)
def add_project_root_to_path():
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, project_root)
