"""Tests for tagging feature."""

from fastapi.testclient import TestClient


class TestAddTags:
    """Test adding tags to prompts."""

    def test_add_tags_to_prompt(self, client: TestClient, sample_prompt_data):
        """Test adding tags to an existing prompt returns 200 with merged tags."""
        # Create a prompt
        create_response = client.post("/prompts", json=sample_prompt_data)
        prompt_id = create_response.json()["id"]

        # Add tags
        response = client.post(
            f"/prompts/{prompt_id}/tags", json={"tags": ["review", "backend"]}
        )

        # Should return 200
        assert response.status_code == 200
        data = response.json()

        # Should have the tags
        assert "tags" in data
        assert "review" in data["tags"]
        assert "backend" in data["tags"]

    def test_add_tags_prompt_not_found(self, client: TestClient):
        """Test adding tags to non-existent prompt returns 404."""
        response = client.post(
            "/prompts/nonexistent-id/tags", json={"tags": ["review"]}
        )
        assert response.status_code == 404
        assert response.json()["detail"] == "Prompt not found"
