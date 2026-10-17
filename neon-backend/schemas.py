from typing import List, Optional, Any, Dict
from pydantic import BaseModel, Field, AliasChoices

class BrandKitSchema(BaseModel):
    id: str = "default"
    brandName: str = Field(default="Neon by Ascertn", validation_alias=AliasChoices("brand_name", "brandName"))
    domain: str = "tryneonai.com"
    primaryColor: str = Field(default="#059669", validation_alias=AliasChoices("primary_color", "primaryColor"))
    secondaryColor: str = Field(default="#0F172A", validation_alias=AliasChoices("secondary_color", "secondaryColor"))
    headingFont: str = Field(default="Plus Jakarta Sans", validation_alias=AliasChoices("heading_font", "headingFont"))
    toneOfVoice: str = Field(default="Bold, clear, executive, action-oriented", validation_alias=AliasChoices("tone_of_voice", "toneOfVoice"))
    targetAudience: str = Field(default="B2B Growth Teams, CMOs, Ecommerce & Agency Leaders", validation_alias=AliasChoices("target_audience", "targetAudience"))

    class Config:
        populate_by_name = True
        from_attributes = True

class BrandKitUpdate(BaseModel):
    brandName: Optional[str] = Field(default=None, validation_alias=AliasChoices("brand_name", "brandName"))
    domain: Optional[str] = None
    primaryColor: Optional[str] = Field(default=None, validation_alias=AliasChoices("primary_color", "primaryColor"))
    secondaryColor: Optional[str] = Field(default=None, validation_alias=AliasChoices("secondary_color", "secondaryColor"))
    headingFont: Optional[str] = Field(default=None, validation_alias=AliasChoices("heading_font", "headingFont"))
    toneOfVoice: Optional[str] = Field(default=None, validation_alias=AliasChoices("tone_of_voice", "toneOfVoice"))
    targetAudience: Optional[str] = Field(default=None, validation_alias=AliasChoices("target_audience", "targetAudience"))

    class Config:
        populate_by_name = True
        from_attributes = True

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
    seoScore: int = Field(default=90, validation_alias=AliasChoices("seo_score", "seoScore"))
    metaTitle: str = Field(default="", validation_alias=AliasChoices("meta_title", "metaTitle"))
    metaDescription: str = Field(default="", validation_alias=AliasChoices("meta_description", "metaDescription"))
    targetKeyword: str = Field(default="", validation_alias=AliasChoices("target_keyword", "targetKeyword"))
    h1: str = ""
    h2s: List[str] = []
    schemaType: str = Field(default="WebPage", validation_alias=AliasChoices("schema_type", "schemaType"))
    canonical: str = ""
    internalLinks: int = Field(default=10, validation_alias=AliasChoices("internal_links", "internalLinks"))
    wordCount: int = Field(default=1200, validation_alias=AliasChoices("word_count", "wordCount"))
    sections: List[SectionSchema] = []
    issues: List[str] = []

    class Config:
        populate_by_name = True
        from_attributes = True

class PageUpdate(BaseModel):
    title: Optional[str] = None
    slug: Optional[str] = None
    status: Optional[str] = None
    metaTitle: Optional[str] = Field(default=None, validation_alias=AliasChoices("meta_title", "metaTitle"))
    metaDescription: Optional[str] = Field(default=None, validation_alias=AliasChoices("meta_description", "metaDescription"))
    targetKeyword: Optional[str] = Field(default=None, validation_alias=AliasChoices("target_keyword", "targetKeyword"))
    h1: Optional[str] = None
    h2s: Optional[List[str]] = None
    schemaType: Optional[str] = Field(default=None, validation_alias=AliasChoices("schema_type", "schemaType"))
    sections: Optional[List[SectionSchema]] = None

    class Config:
        populate_by_name = True
        from_attributes = True

class CampaignSchema(BaseModel):
    id: str
    name: str
    status: str = "Active"
    channels: List[str] = ["Website", "Email", "Social", "SEO"]
    emailsSent: str = Field(default="100,000", validation_alias=AliasChoices("emails_sent", "emailsSent"))
    openRate: str = Field(default="68.4%", validation_alias=AliasChoices("open_rate", "openRate"))
    clickRate: str = Field(default="14.2%", validation_alias=AliasChoices("click_rate", "clickRate"))
    seoKeywordsRanked: int = Field(default=12, validation_alias=AliasChoices("seo_keywords_ranked", "seoKeywordsRanked"))
    visibilityImpact: str = Field(default="+24% Lift", validation_alias=AliasChoices("visibility_impact", "visibilityImpact"))

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
    likesEst: str = Field(default="240+", validation_alias=AliasChoices("likes_est", "likesEst"))

    class Config:
        populate_by_name = True
        from_attributes = True

class EmailBlastSchema(BaseModel):
    campaignName: str = Field(default="Q4 Holiday VIP Access Blast", validation_alias=AliasChoices("campaign_name", "campaignName"))
    audienceSize: int = Field(default=115000, validation_alias=AliasChoices("audience_size", "audienceSize"))
    subjectA: str = Field(default="", validation_alias=AliasChoices("subject_a", "subjectA"))
    subjectB: str = Field(default="", validation_alias=AliasChoices("subject_b", "subjectB"))
    preheader: str = ""
    body: str = ""
    isSending: bool = False
    progress: int = 100
    lastOpenRate: str = Field(default="68.4%", validation_alias=AliasChoices("open_rate", "lastOpenRate"))

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
