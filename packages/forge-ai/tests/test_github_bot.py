from forge_ai.github_bot import post_pr_comment

def test_post_pr_comment_mocked(mocker):
    mock_post = mocker.patch("requests.post")
    mock_post.return_value.status_code = 201
    mock_post.return_value.json.return_value = {"id": 123}
    
    res = post_pr_comment("owner", "repo", 1, "ONGISA Code Audit Report")
    assert res["id"] == 123