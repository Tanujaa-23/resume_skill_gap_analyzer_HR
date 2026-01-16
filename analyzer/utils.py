import PyPDF2
from docx import Document
import re
import string
from collections import Counter
from django.core.files.storage import default_storage


def extract_text_from_pdf(file_path):
    """Extract text from PDF file"""
    try:
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
        return text
    except Exception as e:
        return f"Error extracting PDF: {str(e)}"


def extract_text_from_docx(file_path):
    """Extract text from DOCX file"""
    try:
        doc = Document(file_path)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text
    except Exception as e:
        return f"Error extracting DOCX: {str(e)}"


def extract_text_from_resume(resume_file):
    """Extract text from resume file based on extension"""
    file_path = resume_file.path
    file_extension = resume_file.name.lower().split('.')[-1]
    
    if file_extension == 'pdf':
        return extract_text_from_pdf(file_path)
    elif file_extension == 'docx':
        return extract_text_from_docx(file_path)
    else:
        return "Unsupported file format"


def clean_text(text):
    """Clean and normalize text"""
    # Convert to lowercase
    text = text.lower()
    # Remove extra whitespace and newlines
    text = re.sub(r'\s+', ' ', text)
    # Remove punctuation except for specific cases
    text = re.sub(r'[^\w\s\+\#\.]', ' ', text)
    return text.strip()


def get_predefined_skills():
    """Get predefined skill categories with comprehensive coverage"""
    return {
        'programming_languages': [
            'python', 'python 2', 'python 3', 'java', 'javascript', 'js', 'c++', 'c#', 
            'c', 'php', 'ruby', 'go', 'golang', 'rust', 'swift', 'kotlin', 'scala', 
            'r', 'matlab', 'perl', 'typescript', 'dart', 'objective-c', 'vb.net', 
            'cobol', 'fortran', 'assembly', 'shell', 'bash', 'powershell', 'lua', 
            'haskell', 'elixir', 'clojure', 'groovy', 'f#'
        ],
        'web_technologies': [
            'html', 'html5', 'css', 'css3', 'sass', 'scss', 'less', 'xml', 'json',
            'ajax', 'websocket', 'webrtc', 'responsive design', 'web design',
            'frontend', 'backend', 'full stack', 'fullstack'
        ],
        'frameworks': [
            'django', 'flask', 'fastapi', 'spring', 'spring boot', 'react', 'reactjs',
            'react.js', 'angular', 'angularjs', 'vue', 'vue.js', 'vuejs', 'node.js', 
            'nodejs', 'express', 'express.js', 'laravel', 'symfony', 'codeigniter',
            'rails', 'ruby on rails', 'asp.net', 'mvc', 'bootstrap', 'tailwind', 
            'tailwind css', 'jquery', 'ember.js', 'backbone.js', 'meteor', 'gatsby', 
            'next.js', 'nextjs', 'nuxt.js', 'nuxtjs', 'svelte', 'flutter', 'xamarin',
            'react native', 'ionic', 'cordova', 'electron'
        ],
        'databases': [
            'sql', 'nosql', 'mysql', 'postgresql', 'postgres', 'mongodb', 'mongo',
            'sqlite', 'oracle', 'oracle db', 'sql server', 'mssql', 'redis', 
            'cassandra', 'elasticsearch', 'elastic search', 'dynamodb', 'firebase',
            'firestore', 'couchdb', 'neo4j', 'influxdb', 'mariadb', 'db2', 'sybase', 
            'teradata', 'hbase', 'couchbase', 'rethinkdb'
        ],
        'cloud_platforms': [
            'aws', 'amazon web services', 'azure', 'microsoft azure', 'gcp', 
            'google cloud', 'google cloud platform', 'heroku', 'digitalocean',
            'linode', 'ibm cloud', 'oracle cloud', 'alibaba cloud', 'cloudflare'
        ],
        'tools': [
            'git', 'github', 'gitlab', 'bitbucket', 'docker', 'kubernetes', 'k8s',
            'jenkins', 'travis ci', 'circle ci', 'gitlab ci', 'github actions',
            'ansible', 'terraform', 'vagrant', 'puppet', 'chef', 'saltstack',
            'ci/cd', 'continuous integration', 'continuous deployment',
            'vs code', 'visual studio code', 'sublime text', 'atom', 'vim',
            'intellij', 'pycharm', 'webstorm', 'eclipse', 'netbeans'
        ],
        'build_tools': [
            'webpack', 'gulp', 'grunt', 'maven', 'gradle', 'npm', 'yarn', 'pip',
            'composer', 'make', 'cmake', 'ant', 'babel', 'rollup', 'parcel', 'vite'
        ],
        'testing': [
            'unit testing', 'integration testing', 'tdd', 'bdd', 'test driven development',
            'jest', 'mocha', 'chai', 'jasmine', 'pytest', 'unittest', 'junit', 
            'selenium', 'cypress', 'puppeteer', 'testng', 'cucumber'
        ],
        'project_management': [
            'jira', 'confluence', 'slack', 'trello', 'asana', 'monday', 'notion',
            'basecamp', 'clickup', 'agile', 'scrum', 'kanban', 'waterfall', 'lean'
        ],
        'design_tools': [
            'figma', 'sketch', 'adobe xd', 'photoshop', 'illustrator', 'invision',
            'zeplin', 'balsamiq', 'axure', 'ui/ux', 'ui design', 'ux design'
        ],
        'api_tools': [
            'postman', 'swagger', 'insomnia', 'rest', 'rest api', 'restful', 
            'graphql', 'soap', 'grpc', 'api development', 'api design'
        ],
        'data_science': [
            'machine learning', 'ml', 'artificial intelligence', 'ai', 'deep learning',
            'data science', 'data analysis', 'data analytics', 'data analyst', 'big data', 
            'pandas', 'numpy', 'scikit-learn', 'sklearn', 'tensorflow', 'keras', 'pytorch',
            'opencv', 'nlp', 'natural language processing', 'computer vision',
            'data modeling', 'data modelling', 'statistical analysis', 'statistics',
            'data visualization', 'data visualisation', 'power bi', 'powerbi', 'tableau',
            'looker', 'excel', 'microsoft excel', 'sql', 'r', 'python', 'jupyter',
            'data mining', 'predictive modeling', 'regression', 'classification',
            'clustering', 'neural networks', 'analytics'
        ],
        'education': [
            'bachelor', 'bachelors', 'bachelor degree', 'bachelors degree', 'bsc', 'b.sc',
            'btech', 'b.tech', 'be', 'b.e', 'engineering', 'computer science',
            'information technology', 'it', 'data science', 'statistics', 'mathematics',
            'math', 'maths', 'master', 'masters', 'msc', 'm.sc', 'mtech', 'm.tech',
            'phd', 'doctorate'
        ],
        'concepts': [
            'cloud computing', 'devops', 'microservices', 'api', 'version control',
            'object oriented programming', 'oop', 'functional programming', 
            'design patterns', 'data structures', 'algorithms', 'cybersecurity',
            'blockchain', 'iot', 'internet of things', 'distributed systems',
            'system design', 'software architecture', 'solid principles', 'clean code',
            'problem solving', 'problem-solving', 'analytical skills', 'communication',
            'teamwork', 'collaboration', 'agile methodology'
        ]
    }


def extract_skills_from_text(text):
    """Extract skills from text using predefined skill categories with enhanced matching"""
    cleaned_text = clean_text(text)
    predefined_skills = get_predefined_skills()
    
    found_skills = []
    skill_categories = {}
    
    # Flatten all skills
    all_skills = []
    for category, skills in predefined_skills.items():
        all_skills.extend(skills)
        for skill in skills:
            skill_categories[skill] = category
    
    # Sort skills by length (longest first) to match multi-word skills first
    all_skills.sort(key=len, reverse=True)
    
    # Find skills in text
    for skill in all_skills:
        # Create regex pattern for skill matching (more flexible)
        skill_pattern = skill.lower().replace('.', r'\.')
        pattern = r'\b' + re.escape(skill_pattern) + r's?\b'  # Allow plural forms
        
        if re.search(pattern, cleaned_text):
            # Normalize the skill name for consistent output
            normalized = normalize_skill(skill)
            
            # Check if we already have this skill or its synonym
            already_added = False
            for existing in found_skills:
                if skills_match(skill, existing):
                    already_added = True
                    break
            
            if not already_added:
                found_skills.append(skill)
    
    # Remove duplicates and normalize to title case
    unique_skills = []
    seen_normalized = set()
    
    for skill in found_skills:
        normalized = normalize_skill(skill)
        if normalized not in seen_normalized:
            seen_normalized.add(normalized)
            # Use proper capitalization
            if skill.lower() in ['html', 'html5', 'css', 'css3', 'api', 'rest api', 'seo']:
                unique_skills.append(skill.upper() if len(skill) <= 4 else skill.title())
            else:
                unique_skills.append(skill.title())
    
    return unique_skills


def get_skill_synonyms():
    """Define skill synonyms and variations for better matching"""
    return {
        'javascript': ['js', 'javascript', 'ecmascript'],
        'typescript': ['ts', 'typescript'],
        'python': ['python', 'python 2', 'python 3', 'py'],
        'html': ['html', 'html5'],
        'css': ['css', 'css3'],
        'react': ['react', 'reactjs', 'react.js'],
        'angular': ['angular', 'angularjs', 'angular.js'],
        'vue': ['vue', 'vuejs', 'vue.js'],
        'node': ['node', 'nodejs', 'node.js'],
        'express': ['express', 'expressjs', 'express.js'],
        'mongodb': ['mongodb', 'mongo'],
        'postgresql': ['postgresql', 'postgres'],
        'sql server': ['sql server', 'mssql', 'microsoft sql server'],
        'aws': ['aws', 'amazon web services'],
        'gcp': ['gcp', 'google cloud', 'google cloud platform'],
        'azure': ['azure', 'microsoft azure'],
        'kubernetes': ['kubernetes', 'k8s'],
        'golang': ['go', 'golang'],
        'machine learning': ['machine learning', 'ml'],
        'artificial intelligence': ['artificial intelligence', 'ai'],
        'natural language processing': ['nlp', 'natural language processing'],
        'scikit-learn': ['scikit-learn', 'sklearn', 'scikit learn'],
        'ui/ux': ['ui/ux', 'ui design', 'ux design', 'user interface', 'user experience'],
        'rest api': ['rest', 'rest api', 'rest apis', 'restful', 'restful api', 'api', 'apis'],
        'object oriented programming': ['oop', 'object oriented programming', 'object-oriented'],
        'full stack': ['full stack', 'fullstack', 'full-stack'],
        'ci/cd': ['ci/cd', 'continuous integration', 'continuous deployment'],
        'test driven development': ['tdd', 'test driven development', 'test-driven'],
        'responsive design': ['responsive design', 'responsive web design'],
        'github': ['github', 'git hub'],
        'vs code': ['vs code', 'vscode', 'visual studio code'],
        'bootstrap': ['bootstrap', 'bootstrap 4', 'bootstrap 5'],
        'django': ['django', 'django framework'],
        'mysql': ['mysql', 'my sql'],
        'responsive design': ['responsive design', 'responsive web design', 'web design', 'responsive'],
        'seo': ['seo', 'basic seo', 'search engine optimization'],
        'excel': ['excel', 'microsoft excel', 'ms excel', 'spreadsheet'],
        'power bi': ['power bi', 'powerbi', 'power-bi'],
        'tableau': ['tableau', 'tableau desktop'],
        'sql': ['sql', 'mysql', 'postgresql', 'sql server', 'database', 'databases'],
        'data analysis': ['data analysis', 'data analytics', 'analytics', 'data analyst'],
        'data visualization': ['data visualization', 'data visualisation', 'visualization', 'visualisation'],
        'statistics': ['statistics', 'statistical analysis', 'statistical'],
        'data modeling': ['data modeling', 'data modelling', 'modeling', 'modelling'],
        'problem solving': ['problem solving', 'problem-solving', 'analytical skills', 'analytical'],
        'communication': ['communication', 'communicate', 'presentation'],
        'computer science': ['computer science', 'cs', 'it', 'information technology'],
        'bachelor': ['bachelor', 'bachelors', 'bachelor degree', 'bachelors degree', 'btech', 'be', 'bsc'],
    }



def normalize_skill(skill):
    """Normalize skill name to its canonical form"""
    skill_lower = skill.lower().strip()
    synonyms = get_skill_synonyms()
    
    # Check if skill matches any synonym group
    for canonical, variations in synonyms.items():
        if skill_lower in [v.lower() for v in variations]:
            return canonical
    
    return skill_lower


def skills_match(skill1, skill2):
    """Check if two skills match (considering synonyms)"""
    norm1 = normalize_skill(skill1)
    norm2 = normalize_skill(skill2)
    
    # Direct match
    if norm1 == norm2:
        return True
    
    # Check if they belong to the same synonym group
    synonyms = get_skill_synonyms()
    for canonical, variations in synonyms.items():
        variations_lower = [v.lower() for v in variations]
        if norm1 in variations_lower and norm2 in variations_lower:
            return True
    
    return False


def calculate_skill_match(resume_skills, job_skills):
    """Calculate skill match between resume and job requirements with intelligent matching"""
    resume_skills_lower = [skill.lower().strip() for skill in resume_skills]
    job_skills_lower = [skill.lower().strip() for skill in job_skills]
    
    matched_skills = []
    missing_skills = []
    matched_job_indices = set()
    
    # First pass: exact matching with synonym support
    for i, job_skill in enumerate(job_skills):
        job_skill_lower = job_skill.lower().strip()
        matched = False
        
        for resume_skill in resume_skills:
            resume_skill_lower = resume_skill.lower().strip()
            
            # Check if skills match (including synonyms)
            if skills_match(job_skill_lower, resume_skill_lower):
                if job_skill not in matched_skills:
                    matched_skills.append(job_skill)
                    matched_job_indices.add(i)
                    matched = True
                    break
        
        if not matched:
            missing_skills.append(job_skill)
    
    total_job_skills = len(job_skills)
    matched_count = len(matched_skills)
    
    if total_job_skills == 0:
        match_score = 0
        gap_percentage = 100
    else:
        match_score = (matched_count / total_job_skills) * 100
        gap_percentage = ((total_job_skills - matched_count) / total_job_skills) * 100
    
    return {
        'matched_skills': matched_skills,
        'missing_skills': missing_skills,
        'match_score': round(match_score, 2),
        'gap_percentage': round(gap_percentage, 2)
    }


def determine_readiness_level(match_score):
    """Determine readiness level based on match score"""
    if match_score >= 90:
        return 'HIGHLY_COMPATIBLE'
    elif match_score >= 70:
        return 'JOB_READY'
    elif match_score >= 50:
        return 'INTERMEDIATE'
    else:
        return 'BEGINNER'


def parse_skills_from_string(skills_string):
    """Parse skills from comma-separated string or formatted job descriptions"""
    if not skills_string:
        return []
    
    # Step 1: Handle parentheses - extract both main skill and sub-skills
    # e.g., "AWS (EC2, S3, IAM)" -> ["AWS", "EC2", "S3", "IAM"]
    def extract_with_parentheses(text):
        results = []
        pattern = r'([A-Za-z0-9\s\.\-]+)\s*\(([^\)]+)\)'
        matches = re.findall(pattern, text)
        
        for main, subs in matches:
            main = main.strip()
            if main and len(main) > 1:
                results.append(main)
            # Split sub-skills by comma
            for sub in re.split(r'[,;]\s*', subs):
                sub = sub.strip()
                if sub and len(sub) > 1:
                    results.append(sub)
            # Remove the matched part from text
            text = re.sub(r'[A-Za-z0-9\s\.\-]+\s*\([^\)]+\)', '', text, count=1)
        
        return results, text
    
    paren_skills, skills_string = extract_with_parentheses(skills_string)
    
    # Step 2: Remove category labels (e.g., "Programming Skill:", "Framework:", etc.)
    skills_string = re.sub(r'(?:^|\n|\s)([A-Za-z\s&]+):\s*', ', ', skills_string, flags=re.MULTILINE)
    
    # Step 3: Replace bullets and special characters with commas
    skills_string = re.sub(r'\s*[•\-\*]\s*', ', ', skills_string)
    skills_string = re.sub(r'\s*[\n;]\s*', ', ', skills_string)
    
    # Step 4: Split by comma or 'and'
    skills = re.split(r',|\s+and\s+', skills_string)
    
    # Step 5: Clean each skill
    cleaned_skills = []
    for skill in skills + paren_skills:
        skill = skill.strip()
        
        # Remove asterisks and extra whitespace
        skill = re.sub(r'[\*]+', '', skill)
        skill = re.sub(r'\s+', ' ', skill)
        
        # Skip empty, very short, or invalid skills
        if not skill or len(skill) < 2:
            continue
        
        # Skip common non-skill phrases
        skip_phrases = ['or a related field', 'proven experience', 'strong proficiency',
                       'experience with', 'knowledge of', 'ability to', 'e.g.', 'such as',
                       'understanding', 'concepts']
        if any(phrase in skill.lower() for phrase in skip_phrases):
            continue
        
        # Skip if it's just a category name
        if skill.endswith(':'):
            continue
        
        cleaned_skills.append(skill)
    
    # Remove duplicates while preserving order
    seen = set()
    unique_skills = []
    for skill in cleaned_skills:
        skill_lower = skill.lower()
        if skill_lower not in seen:
            seen.add(skill_lower)
            unique_skills.append(skill)
    
    return unique_skills


def format_skills_list(skills_list):
    """Format skills list to comma-separated string"""
    if not skills_list:
        return ""
    return ", ".join(skills_list)


def get_skill_suggestions(missing_skills, matched_skills):
    """Generate professional skill improvement suggestions"""
    suggestions = []
    
    # Case 1: No skills extracted at all
    if not missing_skills and not matched_skills:
        suggestions.append("⚠️ Unable to extract skills from the resume. Please ensure your resume includes:")
        suggestions.append("📚 Technical skills (programming languages, frameworks, tools)")
        suggestions.append("📚 Specific technologies you've worked with")
        suggestions.append("📚 Clear skill sections or project descriptions")
        suggestions.append("💡 Tip: Use standard skill names like 'Python', 'JavaScript', 'SQL', etc.")
        return suggestions
    
    # Case 2: All skills matched
    if not missing_skills and matched_skills:
        suggestions.append("✓ Excellent! You possess all the required skills for this position. Your profile demonstrates strong alignment with the job requirements.")
        return suggestions
    
    # Case 3: Some skills missing
    # Categorize missing skills
    predefined_skills = get_predefined_skills()
    skill_categories = {}
    for category, skills in predefined_skills.items():
        for skill in skills:
            skill_categories[skill.lower()] = category.replace('_', ' ').title()
    
    categorized_missing = {}
    for skill in missing_skills:
        skill_normalized = normalize_skill(skill)
        category = skill_categories.get(skill_normalized, 'Technical Skills')
        if category not in categorized_missing:
            categorized_missing[category] = []
        categorized_missing[category].append(skill)
    
    # Generate professional suggestions by category
    priority_order = ['Programming Languages', 'Web Technologies', 'Frameworks', 'Databases', 
                     'Cloud Platforms', 'Devops Tools', 'Data Science', 'Technical Skills']
    
    for category in priority_order:
        if category in categorized_missing:
            skills = categorized_missing[category]
            if len(skills) == 1:
                suggestions.append(f"📚 Develop proficiency in {skills[0]} to strengthen your {category} expertise.")
            elif len(skills) == 2:
                suggestions.append(f"📚 Focus on mastering {skills[0]} and {skills[1]} to enhance your {category} capabilities.")
            else:
                skills_str = ", ".join(skills[:3])
                if len(skills) > 3:
                    skills_str += f" and {len(skills) - 3} more"
                suggestions.append(f"📚 Prioritize learning {skills_str} to build comprehensive {category} skills.")
    
    # Add remaining categories not in priority order
    for category, skills in categorized_missing.items():
        if category not in priority_order:
            if len(skills) == 1:
                suggestions.append(f"📚 Consider gaining experience with {skills[0]}.")
            else:
                skills_str = ", ".join(skills[:2])
                suggestions.append(f"📚 Expand your knowledge in {skills_str}.")
    
    # Add actionable advice based on gap size
    gap_size = len(missing_skills)
    if gap_size <= 3:
        suggestions.append("💡 You're close to meeting all requirements! Focus on these few skills to become a perfect match.")
    elif gap_size <= 6:
        suggestions.append("💡 Prioritize the most critical skills first. Consider online courses, certifications, or hands-on projects.")
    else:
        suggestions.append("💡 Create a structured learning plan. Start with foundational skills and progressively build expertise.")
        suggestions.append("💡 Consider bootcamps, online platforms (Coursera, Udemy, Pluralsight), or mentorship programs.")
    
    # Add general professional advice
    suggestions.append("🎯 Build a portfolio showcasing projects that demonstrate these skills in real-world scenarios.")
    suggestions.append("🔗 Engage with professional communities, attend workshops, and contribute to open-source projects.")
    
    return suggestions