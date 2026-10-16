from typing import List, Optional, Any, Dict
from pydantic import BaseModel, Field

class BrandKitSchema(BaseModel):
    id: str = "default"
    brandName: str = Field(default="Neon by Ascertn", alias="brand_name")
    domain: str = "tryneonai.com"
    primaryColor: str = Field(default="#059669", alias="primary_color")
    secondaryColor: str = Field(default="#0F172A", alias="secondary_color")
    headingFont: str = Field(default="Plus Jakarta Sans", alias="heading_font")
    toneOfVoice: str = Field(default="Bold, clear, executive, action-oriented", alias="tone_of_voice")
    targetAudience: str = Field(default="B2B Growth Teams, CMOs, Ecommerce & Agency Leaders", alias="target_audience")

    class Config:
        populate_by_name = True
        from_attributes = True

class BrandKitUpdate(BaseModel):
    brandName: Optional[str] = None
    domain: Optional[str] = None
    primaryColor: Optional[str] = None
    secondaryColor: Optional[str] = None
    headingFont: Optional[str] = None
    toneOfVoice: Optional[str] = None
    targetAudience: Optional[str] = None

class SectionSchema(BaseModel):
    id: str
    type: str
    heading: str
    subheading: str

class PageSchema(BaseModel):
    id: str
    title: str
    slug: str
    status: str = "Published"
    views: str = "1,204"
    seoScore: int = Field(default=90, alias="seo_score")
    metaTitle: str = Field(default="", alias="meta_title")
    metaDescription: str = Field(default="", alias="meta_description")
    targetKeyword: str = Field(default="", alias="target_keyword")
    h1: str = ""
    h2s: List[str] = []
    schemaType: str = Field(default="WebPage", alias="schema_type")
    canonical: str = ""
    internalLinks: int = Field(default=10, alias="internal_links")
    wordCount: int = Field(default=1200, alias="word_count")
    sections: List[SectionSchema] = []
    issues: List[str] = []

    class Config:
        populate_by_name = True
        from_attributes = True

class PageUpdate(BaseModel):
    title: Optional[str] = None
    slug: Optional[str] = None
    status: Optional[str] = None
    metaTitle: Optional[str] = None
    metaDescription: Optional[str] = None
    targetKeyword: Optional[str] = None
    h1: Optional[str] = None
    h2s: Optional[List[str]] = None
    schemaType: Optional[str] = None
    sections: Optional[List[SectionSchema]] = None

class CampaignSchema(BaseModel):
    id: str
    name: str
    status: str = "Active"
    channels: List[str] = ["Website", "Email", "Social", "SEO"]
    emailsSent: str = Field(default="100,000", alias="emails_sent")
    openRate: str = Field(default="68.4%", alias="open_rate")
    clickRate: str = Field(default="14.2%", alias="click_rate")
    seoKeywordsRanked: int = Field(default=12, alias="seo_keywords_ranked")
    visibilityImpact: str = Field(default="+24% Lift", alias="visibility_impact")

    class Config:
        populate_by_name = True
        from_attributes = True

class TaskItemSchema(BaseModel):
    id: str
    title: str
    due: str = "Today"
    type: str = "SEO"
    done: bool = False

    class Config:
        from_attributes = True

class TaskToggleRequest(BaseModel):
    done: Optional[bool] = None

class SocialPostSchema(BaseModel):
    id: str
    platform: str
    day: str
    status: str = "Scheduled"
    content: str
    likesEst: str = Field(default="240+", alias="likes_est")

    class Config:
        populate_by_name = True
        from_attributes = True

class EmailBlastSchema(BaseModel):
    campaignName: str = Field(default="Q4 Holiday VIP Access Blast", alias="campaign_name")
    audienceSize: int = Field(default=115000, alias="audience_size")
    subjectA: str = Field(default="", alias="subject_a")
    subjectB: str = Field(default="", alias="subject_b")
    preheader: str = ""
    body: str = ""
    isSending: bool = False
    progress: int = 100
    lastOpenRate: str = Field(default="68.4%", alias="open_rate")

    class Config:
        populate_by_name = True
        from_attributes = True

class VisibilityMetricsSchema(BaseModel):
    totalScore: int
    technicalSeo: int
    contentFreshness: int
    campaignReach: int
    seoStatusLabel: str

class WorkspaceBootstrapResponse(BaseModel):
    pages: List[PageSchema]
    campaigns: List[CampaignSchema]
    tasks: List[TaskItemSchema]
    brandKit: BrandKitSchema
    socialPosts: List[SocialPostSchema]
    emailBlast: EmailBlastSchema
    visibilityMetrics: VisibilityMetricsSchema

class AskNeonRequest(BaseModel):
    prompt: str
    brandKit: Optional[Dict[str, Any]] = None
    apiKey: Optional[str] = None

class AskNeonResponse(BaseModel):
    success: bool
    data: Dict[str, Any]
    hydrated: Dict[str, Any]
    visibilityMetrics: VisibilityMetricsSchema

class SeoAuditRequest(BaseModel):
    url: str
    targetKeyword: Optional[str] = ""

class SeoDiagnostics(BaseModel):
    title: str = ""
    metaDescription: str = ""
    h1: str = ""
    allH1s: List[str] = []
    h2s: List[str] = []
    canonical: str = ""
    hasJsonLd: bool = False
    schemaType: str = "WebPage"
    internalLinks: int = 0
    wordCount: int = 0
    titlePixelEst: int = 0
    issues: List[str] = []

class SeoAuditResponse(BaseModel):
    success: bool
    targetUrl: str
    status: int
    seoScore: int
    diagnostics: SeoDiagnostics

class AutoFixRequest(BaseModel):
    targetKeyword: Optional[str] = None
    currentMetadata: Optional[Dict[str, Any]] = None
    apiKey: Optional[str] = None

class KeywordClusterRequest(BaseModel):
    seedKeyword: str
    apiKey: Optional[str] = None

class KeywordClusterItem(BaseModel):
    cluster: str
    intent: str
    volume: str
    difficulty: str
    recSlug: str

class KeywordClusterResponse(BaseModel):
    success: bool
    seedKeyword: str
    clusters: List[KeywordClusterItem]

class EmailBatchRequest(BaseModel):
    campaignName: Optional[str] = "High-Velocity Omnichannel Blast"
    audienceSize: Optional[int] = 100000
    subjectA: Optional[str] = ""
    subjectB: Optional[str] = ""
    preheader: Optional[str] = ""
    body: Optional[str] = ""
