"""Tests for formatting utilities."""

import pytest
from src.utils.formatting import format_duration, calculate_rest_duration


class TestFormatDuration:
    """Tests for format_duration function."""
    
    def test_zero_seconds(self):
        assert format_duration(0) == "00:00:00"
    
    def test_seconds_only(self):
        assert format_duration(45) == "00:00:45"
    
    def test_minutes_and_seconds(self):
        assert format_duration(125) == "00:02:05"
    
    def test_hours_minutes_seconds(self):
        assert format_duration(3661) == "01:01:01"
    
    def test_large_hours(self):
        assert format_duration(36000) == "10:00:00"


class TestCalculateRestDuration:
    """Tests for calculate_rest_duration function."""
    
    def test_minimum_rest(self):
        # Even 0 work should give minimum 5 min rest
        assert calculate_rest_duration(0) == 300  # 5 minutes
    
    def test_short_work_gets_minimum(self):
        # 10 minutes work should still give 5 min rest
        assert calculate_rest_duration(600) == 300
    
    def test_25_minutes_work(self):
        # 25 minutes work = 5 minutes rest
        assert calculate_rest_duration(1500) == 300
    
    def test_50_minutes_work(self):
        # 50 minutes work = 10 minutes rest
        assert calculate_rest_duration(3000) == 600
    
    def test_partial_period(self):
        # 30 minutes work = 10 minutes rest (25 + partial)
        assert calculate_rest_duration(1800) == 600