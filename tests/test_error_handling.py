#!/usr/bin/env python

import pytest
from unittest.mock import patch, MagicMock
import server
from server import execute_query, list_tables, get_table_schema, sample_table_data

class TestErrorHandling:
    @pytest.mark.asyncio
    async def test_kusto_client_exception(self, monkeypatch):
        """Test that the tools handle exceptions from the KustoClient."""
        # Save original config values
        original_cluster = server.config.cluster_url
        original_database = server.config.database
        original_tenant_id = server.config.tenant_id
        original_client_id = server.config.client_id
        original_client_secret = server.config.client_secret
        
        try:
            # Set test configuration
            server.config.cluster_url = "https://testcluster.region.kusto.windows.net"
            server.config.database = "testdb"
            server.config.tenant_id = "test-tenant-id"
            server.config.client_id = "test-client-id"
            server.config.client_secret = "test-client-secret"
            
            error_message = "Kusto client error"
            
            # Mock the KustoClient to raise an exception
            with patch('server.get_kusto_client') as mock_get_client:
                mock_client = MagicMock()
                mock_client.execute.side_effect = Exception(error_message)
                mock_get_client.return_value = mock_client
                
                # Test execute_query
                with pytest.raises(Exception) as excinfo:
                    await execute_query("test query")
                assert error_message in str(excinfo.value)
                
                # Test list_tables
                with pytest.raises(Exception) as excinfo:
                    await list_tables()
                assert error_message in str(excinfo.value)
                
                # Test get_table_schema
                with pytest.raises(Exception) as excinfo:
                    await get_table_schema("test_table")
                assert error_message in str(excinfo.value)
                
                # Test sample_table_data
                with pytest.raises(Exception) as excinfo:
                    await sample_table_data("test_table")
                assert error_message in str(excinfo.value)
        finally:
            # Restore original config
            server.config.cluster_url = original_cluster
            server.config.database = original_database
            server.config.tenant_id = original_tenant_id
            server.config.client_id = original_client_id
            server.config.client_secret = original_client_secret
    
    @pytest.mark.asyncio
    async def test_malformed_result_set(self, monkeypatch):
        """Test handling of malformed result sets from the KustoClient."""
        # Save original config values
        original_cluster = server.config.cluster_url
        original_database = server.config.database
        original_tenant_id = server.config.tenant_id
        original_client_id = server.config.client_id
        original_client_secret = server.config.client_secret
        
        try:
            # Set test configuration
            server.config.cluster_url = "https://testcluster.region.kusto.windows.net"
            server.config.database = "testdb"
            server.config.tenant_id = "test-tenant-id"
            server.config.client_id = "test-client-id"
            server.config.client_secret = "test-client-secret"
            
            # Mock the KustoClient to return malformed results
            with patch('server.get_kusto_client') as mock_get_client:
                mock_client = MagicMock()
                
                # Create a malformed result with missing elements
                malformed_result = MagicMock()
                malformed_result.primary_results = [MagicMock()]
                # No columns or rows defined
                
                mock_client.execute.return_value = malformed_result
                mock_get_client.return_value = mock_client
                
                # This should not raise an exception, but return an empty list
                result = await execute_query("test query")
                assert result == []
        finally:
            # Restore original config
            server.config.cluster_url = original_cluster
            server.config.database = original_database
            server.config.tenant_id = original_tenant_id
            server.config.client_id = original_client_id
            server.config.client_secret = original_client_secret
