"""
FILTER MODULE
━━━━━━━━━━━━
Decides which scraped jobs are worth alerting on.
Edit INCLUDE_KEYWORDS / EXCLUDE_KEYWORDS to tune signal vs noise.

Targets junior-to-mid software engineering roles with a
backend / full-stack focus (Node.js, Java/Spring, Python/FastAPI,
React/Next.js, AWS). Hybrid SWE + RAG/LLM roles are also included.
"""

# ── Tune these ────────────────────────────────────────────────────────────────
INCLUDE_KEYWORDS = [
    # Generic role titles
    "software engineer", "software developer", "software development engineer",
    "sde", "swe",
    "application developer", "application engineer",
    "product engineer",

    # Backend
    "backend engineer", "back-end engineer", "back end engineer",
    "backend developer", "back-end developer", "back end developer",
    "api engineer", "api developer",
    "server engineer", "services engineer",

    # Full-stack
    "full stack", "full-stack", "fullstack",

    # Cloud / platform (matches SAA-C03 certification signal)
    "cloud engineer", "cloud developer",
    "platform engineer", "platform developer",
    "aws engineer", "aws developer",

    # Language / framework specific titles
    "node.js", "nodejs", "node developer", "node engineer",
    "java developer", "java engineer", "spring boot", "spring developer",
    "python developer", "python engineer", "fastapi",
    "typescript developer", "typescript engineer",
    "react developer", "react engineer", "next.js", "nextjs",

    # Early-career signals
    "graduate software", "graduate engineer", "graduate developer",
    "junior software", "junior developer", "junior engineer",
    "associate software", "associate developer", "associate engineer",

    # Hybrid SWE + AI (secondary target)
    "ai engineer", "genai engineer", "llm engineer",
    "langchain", "rag ",
]

# NOTE: All EXCLUDE_KEYWORDS must be lowercase — the haystack is lowercased
# before matching. Excludes are checked against the job title ONLY (not the
# company name), so short prefixes like "senior " are safe and will not kill
# legitimate SWE jobs at companies whose name contains those words.
EXCLUDE_KEYWORDS = [
    # Seniority above target band. Short prefixes catch every stack-specific
    # variant ("Senior Backend Engineer", "Principal Full Stack Developer",
    # "Staff Cloud Engineer", "Lead Node.js Developer", etc.).
    "senior ", "sr. ", "sr ",
    "principal ", "staff ", "lead ",
    "tech lead", "technical lead",
    "engineering manager", "software manager", " manager",
    "head of", "vp of", "vice president",
    "director of", "director,",
    " cto", " cio",
    "architect", "professor",

    # Adjacent tracks that aren't SWE
    "product manager", "project manager", "program manager",
    "scrum master", "business analyst",
    "designer", "ux ", " ui ",
    "hardware", "firmware", "embedded",
    "game developer", "game engineer",
    "mobile developer", "android developer", "ios developer",

    # Stacks outside the resume
    ".net developer", "dotnet developer",
    "c# developer", "c#/", "c# engineer",
    ".net engineer", ".net developer",
    "php developer", "wordpress",
    "ruby on rails", "rails developer",
    "salesforce developer", "salesforce admin",
    "sap consultant", "abap developer",
    "mainframe", "cobol",

    # Non-relevant openings
    "unpaid", "volunteer",
    "sales", "marketing", "recruiter",
]
# ──────────────────────────────────────────────────────────────────────────────


def is_relevant(job: dict) -> bool:
    """Return True if the job matches our filter criteria.

    Includes are checked against title + company (permissive discovery).
    Excludes are checked against the title only (precise role filtering).
    """
    title = job["title"].lower()
    haystack = f"{title} {job['company'].lower()}"

    if not any(kw in haystack for kw in INCLUDE_KEYWORDS):
        return False

    if any(kw in title for kw in EXCLUDE_KEYWORDS):
        return False

    return True


def filter_jobs(jobs: list[dict]) -> list[dict]:
    return [j for j in jobs if is_relevant(j)]
