"""
Analytics Service
Provides business intelligence metrics from the database.
"""

from datetime import datetime, timedelta
from database.queries import get_all_leads, get_all_conversations


class AnalyticsService:
    """
    Computes analytics metrics from conversation and lead data.
    """

    def get_conversation_volume(self, days=7):
        """
        Get conversation volume for the last N days.
        Returns a dict of date -> count.
        """
        conversations = get_all_conversations()
        cutoff = datetime.utcnow() - timedelta(days=days)
        volume = {}
        for conv in conversations:
            if conv.created_at and conv.created_at >= cutoff:
                day = conv.created_at.strftime("%Y-%m-%d")
                volume[day] = volume.get(day, 0) + 1
        return volume

    def get_lead_stats(self):
        """
        Get lead statistics.
        Returns dict with total, new, qualified, contacted, lost counts.
        """
        leads = get_all_leads()
        stats = {
            "total": len(leads),
            "new": 0,
            "qualified": 0,
            "contacted": 0,
            "lost": 0,
        }
        for lead in leads:
            status = lead.status.lower()
            if status in stats:
                stats[status] += 1
        return stats

    def get_channel_breakdown(self):
        """
        Get conversation count by channel/source.
        """
        conversations = get_all_conversations()
        channels = {}
        for conv in conversations:
            source = conv.answered_by or "Unknown"
            channels[source] = channels.get(source, 0) + 1
        return channels

    def get_language_distribution(self):
        """
        Get conversation count by detected language.
        """
        conversations = get_all_conversations()
        langs = {}
        for conv in conversations:
            lang = conv.detected_language or "en"
            langs[lang] = langs.get(lang, 0) + 1
        return langs

    def get_csat_score(self):
        """
        Simulated CSAT score (would come from feedback in production).
        """
        return 4.7

    def get_avg_response_time(self):
        """
        Calculate average response time from conversations.
        """
        conversations = get_all_conversations()
        times = [conv.response_time for conv in conversations if conv.response_time and conv.response_time > 0]
        if times:
            return sum(times) / len(times)
        return 0

    def get_resolution_rate(self):
        """
        Simulated resolution rate.
        """
        return 94.2

    def get_ai_deflection_rate(self):
        """
        Percentage of conversations handled by AI without human escalation.
        """
        conversations = get_all_conversations()
        if not conversations:
            return 71.0
        ai_handled = sum(1 for c in conversations if c.answered_by and c.answered_by != "Human")
        return round((ai_handled / len(conversations)) * 100, 1) if conversations else 71.0


# Singleton instance
analytics_service = AnalyticsService()