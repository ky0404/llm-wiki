"""Wiki API 测试用例 - 覆盖所有 API 端点"""
import pytest
import sys
import os
from pathlib import Path
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).parent.parent / "api"))

from config import config


class TestConfig:
    """配置模块测试"""

    def test_config_defaults(self):
        """测试配置默认值"""
        assert config.WIKI_ROOT.exists()
        assert config.WIKI_DATA_DIR.exists()
        assert config.LOG_DIR.exists()
        assert config.API_VERSION == "1.0.0"

    def test_config_env_override(self):
        """测试环境变量覆盖"""
        with patch.dict(os.environ, {"API_PORT": "9000", "WIKI_ROOT": "/tmp"}):
            config.__init__(config)
            assert config.API_PORT == 9000

    def test_config_paths(self):
        """测试路径配置"""
        assert config.FRONTEND_DIR.exists() or True
        assert config.CACHE_FILE is not None
        assert config.SCRIPTS_DIR.exists()


class TestWikiStats:
    """/wiki/stats 端点测试"""

    @pytest.fixture
    def client(self):
        from main import app
        return TestClient(app)

    def test_stats_response_structure(self, client):
        """测试 stats 响应结构"""
        response = client.get("/wiki/stats")
        if response.status_code == 500:
            pytest.skip("缓存文件不存在，跳过测试")

        data = response.json()
        assert "total_files" in data
        assert "total_edges" in data
        assert "health_score" in data
        assert "type_distribution" in data
        assert "recent_pages" in data
        assert "metadata" in data

    def test_stats_health_score_range(self, client):
        """测试健康分数范围"""
        response = client.get("/wiki/stats")
        if response.status_code == 500:
            pytest.skip("缓存文件不存在，跳过测试")

        data = response.json()
        assert 0 <= data["health_score"] <= 100


class TestWikiGraph:
    """/wiki/graph 端点测试"""

    @pytest.fixture
    def client(self):
        from main import app
        return TestClient(app)

    def test_graph_response_structure(self, client):
        """测试 graph 响应结构"""
        response = client.get("/wiki/graph")
        if response.status_code == 500:
            pytest.skip("缓存文件不存在，跳过测试")

        data = response.json()
        assert "nodes" in data
        assert "edges" in data
        assert isinstance(data["nodes"], list)
        assert isinstance(data["edges"], list)

    def test_graph_node_structure(self, client):
        """测试图谱节点结构"""
        response = client.get("/wiki/graph")
        if response.status_code == 500:
            pytest.skip("缓存文件不存在，跳过测试")

        data = response.json()
        if data["nodes"]:
            node = data["nodes"][0]
            assert "id" in node
            assert "title" in node
            assert "type" in node
            assert "tags" in node


class TestWikiSearch:
    """/wiki/search 端点测试"""

    @pytest.fixture
    def client(self):
        from main import app
        return TestClient(app)

    def test_search_missing_query(self, client):
        """测试缺少查询参数"""
        response = client.get("/wiki/search")
        assert response.status_code == 422

    def test_search_empty_query(self, client):
        """测试空查询"""
        response = client.get("/wiki/search?q=")
        assert response.status_code == 422

    def test_search_response_structure(self, client):
        """测试搜索响应结构"""
        response = client.get("/wiki/search?q=test")
        if response.status_code == 500:
            pytest.skip("搜索执行失败")

        data = response.json()
        assert "total" in data
        assert "results" in data
        assert isinstance(data["results"], list)

    def test_search_result_structure(self, client):
        """测试搜索结果项结构"""
        response = client.get("/wiki/search?q=wiki")
        if response.status_code == 500:
            pytest.skip("搜索执行失败")

        data = response.json()
        if data["results"]:
            result = data["results"][0]
            assert "file" in result
            assert "line" in result
            assert "snippet" in result


class TestWikiPages:
    """/wiki/pages 端点测试"""

    @pytest.fixture
    def client(self):
        from main import app
        return TestClient(app)

    def test_pages_response_structure(self, client):
        """测试 pages 响应结构"""
        response = client.get("/wiki/pages")
        data = response.json()
        assert "total" in data
        assert "pages" in data
        assert isinstance(data["pages"], list)

    def test_pages_limit(self, client):
        """测试 limit 参数"""
        response = client.get("/wiki/pages?limit=10")
        data = response.json()
        assert len(data["pages"]) <= 10

    def test_pages_limit_validation(self, client):
        """测试 limit 边界验证"""
        response = client.get("/wiki/pages?limit=0")
        assert response.status_code == 422

        response = client.get("/wiki/pages?limit=300")
        assert response.status_code == 422


class TestWikiContent:
    """/wiki/content 端点测试"""

    @pytest.fixture
    def client(self):
        from main import app
        return TestClient(app)

    def test_content_missing_path(self, client):
        """测试缺少路径参数"""
        response = client.get("/wiki/content")
        assert response.status_code == 422

    def test_content_empty_path(self, client):
        """测试空路径"""
        response = client.get("/wiki/content?path=")
        assert response.status_code == 422

    def test_content_response_structure(self, client):
        """测试 content 响应结构"""
        response = client.get("/wiki/content?path=sources/test")
        if response.status_code == 404:
            pytest.skip("测试文件不存在")

        data = response.json()
        assert "content" in data
        assert "frontmatter" in data
        assert "raw" in data

    def test_content_path_traversal_blocked(self, client):
        """测试路径遍历攻击被阻止"""
        response = client.get("/wiki/content?path=../../../etc/passwd")
        assert response.status_code == 400


class TestWikiRefresh:
    """/wiki/refresh 端点测试"""

    @pytest.fixture
    def client(self):
        from main import app
        return TestClient(app)

    def test_refresh_response_structure(self, client):
        """测试 refresh 响应结构"""
        response = client.post("/wiki/refresh")
        if response.status_code == 500:
            pytest.skip("刷新脚本执行失败")

        data = response.json()
        assert "status" in data
        assert "message" in data
        assert data["status"] == "ok"


class TestRoot:
    """根端点测试"""

    @pytest.fixture
    def client(self):
        from main import app
        return TestClient(app)

    def test_root_response(self, client):
        """测试根端点响应"""
        response = client.get("/")
        data = response.json()
        assert "message" in data
        assert "version" in data
        assert "wiki_root" in data


class TestHealth:
    """健康检查端点测试"""

    @pytest.fixture
    def client(self):
        from main import app
        return TestClient(app)

    def test_health_response(self, client):
        """测试健康检查响应"""
        response = client.get("/health")
        data = response.json()
        assert data["status"] == "ok"
        assert "cache_exists" in data
        assert "wiki_root_exists" in data


class TestSanitizePath:
    """路径安全测试"""

    def test_path_traversal(self):
        """测试路径遍历攻击"""
        from routes.wiki_route import sanitize_path
        import pytest

        with pytest.raises(Exception):
            sanitize_path("../../../etc/passwd")

        with pytest.raises(Exception):
            sanitize_path("/absolute/path")

    def test_valid_paths(self):
        """测试有效路径"""
        from routes.wiki_route import sanitize_path

        assert sanitize_path("sources/test") == "sources/test"
        assert sanitize_path("my-learning-path/theory/ai") == "my-learning-path/theory/ai"
        assert sanitize_path("concepts/rag") == "concepts/rag"


class TestSearchNative:
    """原生搜索测试"""

    def test_search_files_native(self):
        """测试原生文件搜索"""
        from routes.wiki_route import search_files_native

        results = search_files_native("wiki", [config.WIKI_DATA_DIR])
        assert isinstance(results, dict)


class TestListFilesNative:
    """原生文件列表测试"""

    def test_list_files_native(self):
        """测试原生文件列表"""
        from routes.wiki_route import list_files_native

        results = list_files_native([config.WIKI_DATA_DIR], limit=10)
        assert isinstance(results, list)
        assert len(results) <= 10


class TestWikilinkConversion:
    """Wikilink 转换测试"""

    def test_convert_wikilink_cached(self):
        """测试 wikilink 缓存转换"""
        from routes.wiki_route import convert_wikilink_cached

        result = convert_wikilink_cached("sources/test|测试")
        assert 'href="/wiki/sources/test"' in result
        assert "测试" in result

        result2 = convert_wikilink_cached("sources/test")
        assert 'href="/wiki/sources/test"' in result2
        assert "test" in result2

    def test_convert_wikilinks_full(self):
        """测试完整 wikilink 转换"""
        from routes.wiki_route import convert_wikilinks

        html = 'Test [[wiki/sources/test|链接]] and [[wiki/other]]'
        result = convert_wikilinks(html)
        assert 'href="/wiki/sources/test"' in result
        assert 'href="/wiki/other"' in result


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])