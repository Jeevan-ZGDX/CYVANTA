from datetime import datetime
from typing import Any, List
from sqlalchemy import Column, String, Integer, Boolean, DateTime, JSON, Text
from database import Base

class BrandKit(Base):
    __tablename__ = "brand_kits"

    id = Column(String(50), primary_key=True, default="default")
    brand_name = Column(String(100), default="Neon by Ascertn")
    domain = Column(String(100), default="tryneonai.com")
    primary_color = Column(String(20), default="#059669")
    secondary_color = Column(String(20), default="#0F172A")
    heading_font = Column(String(50), default="Plus Jakarta Sans")
    tone_of_voice = Column(String(255), default="Bold, clear, executive, action-oriented")
    target_audience = Column(String(255), default="B2B Growth Teams, CMOs, Ecommerce & Agency Leaders")
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Page(Base):
    __tablename__ = "pages"

    id = Column(String(100), primary_key=True)
    title = Column(String(255), nullable=False)
    slug = Column(String(255), nullable=False, unique=True)
    status = Column(String(50), default="Published")
    views = Column(String(50), default="1,204")
    seo_score = Column(Integer, default=90)
    meta_title = Column(String(255), default="")
    meta_description = Column(Text, default="")
    target_keyword = Column(String(255), default="")
    h1 = Column(String(255), default="")
    h2s = Column(JSON, default=list)  # list of strings
    schema_type = Column(String(100), default="WebPage")
    canonical = Column(String(255), default="")
    internal_links = Column(Integer, default=10)
    word_count = Column(Integer, default=1200)
    sections = Column(JSON, default=list)  # list of section objects: {id, type, heading, subheading}
    issues = Column(JSON, default=list)  # list of issue strings
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Campaign(Base):
    __tablename__ = "campaigns"

    id = Column(String(100), primary_key=True)
    name = Column(String(255), nullable=False)
    status = Column(String(50), default="Active")
    channels = Column(JSON, default=lambda: ["Website", "Email", "Social", "SEO"])
    emails_sent = Column(String(50), default="100,000")
    open_rate = Column(String(50), default="68.4%")
    click_rate = Column(String(50), default="14.2%")
    seo_keywords_ranked = Column(Integer, default=12)
    visibility_impact = Column(String(50), default="+24% Lift")
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class TaskItem(Base):
    __tablename__ = "task_items"

    id = Column(String(100), primary_key=True)
    title = Column(String(255), nullable=False)
    due = Column(String(50), default="Today")
    type = Column(String(50), default="SEO")
    done = Column(Boolean, default=False)

class SocialPost(Base):
    __tablename__ = "social_posts"

    id = Column(String(100), primary_key=True)
    platform = Column(String(50), default="LinkedIn")
    day = Column(String(50), default="Tomorrow · 9:00 AM")
    status = Column(String(50), default="Scheduled")
    content = Column(Text, nullable=False)
    likes_est = Column(String(50), default="240+")

class EmailBlastJob(Base):
    __tablename__ = "email_blast_jobs"

    id = Column(String(100), primary_key=True)
    campaign_name = Column(String(255), default="Q4 Holiday VIP Access Blast")
    audience_size = Column(Integer, default=115000)
    subject_a = Column(String(255), default="")
    subject_b = Column(String(255), default="")
    preheader = Column(String(255), default="")
    body = Column(Text, default="")
    status = Column(String(50), default="Completed")
    progress = Column(Integer, default=100)
    open_rate = Column(String(50), default="68.4%")
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
