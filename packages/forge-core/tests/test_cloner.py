from forge_core.repository.cloner import clone_github_repository
import os

def test_cloner_creates_temp_dir(mocker):
    mocker.patch("subprocess.run", return_value=mocker.Mock(returncode=0))
    path = clone_github_repository("Nash6643", "forge")
    assert isinstance(path, str)