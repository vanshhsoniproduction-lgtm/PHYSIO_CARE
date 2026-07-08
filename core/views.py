from django.shortcuts import render
from appointments.models import Review


# Service data dictionary for the detail pages
SERVICES = {
    "spine-care": {
        "title": "Spine & Disc Care",
        "subtitle": "Advanced Spinal Rehabilitation",
        "icon": "accessibility_new",
        "color": "#8b5cf6",
        "color_light": "rgba(139, 92, 246, 0.1)",
        "hero_desc": "Specialized PIVD care, posture correction protocols, and advanced spinal rehabilitation for lasting relief and restored mobility.",
        "overview": "Our Spine & Disc Care program combines advanced manual therapy techniques with evidence-based rehabilitation protocols to address the root cause of spinal disorders. With over 20 years of specialization, Dr. Bhubon Chatterji has developed proprietary treatment methodologies that have helped thousands of patients avoid surgery and regain their quality of life.",
        "benefits": [
            {"icon": "healing", "title": "Non-Surgical Solutions", "desc": "Advanced conservative treatments that address disc herniations and spinal stenosis without surgery."},
            {"icon": "straighten", "title": "Posture Correction", "desc": "Comprehensive postural assessment and correction programs for long-term spinal health."},
            {"icon": "self_improvement", "title": "Core Stabilization", "desc": "Targeted strengthening protocols to build a natural spinal support system."},
            {"icon": "monitor_heart", "title": "Pain Management", "desc": "Multi-modal pain relief strategies combining manual therapy, electrotherapy, and exercise."},
        ],
        "conditions": ["Herniated Disc (PIVD)", "Sciatica", "Cervical Spondylosis", "Lumbar Spondylosis", "Spinal Stenosis", "Degenerative Disc Disease", "Scoliosis", "Postural Dysfunction"],
        "process": [
            {"step": "1", "title": "Comprehensive Assessment", "desc": "In-depth spinal examination with movement analysis and diagnostic review."},
            {"step": "2", "title": "Custom Treatment Plan", "desc": "Personalized protocol combining manual therapy, exercises, and modalities."},
            {"step": "3", "title": "Active Rehabilitation", "desc": "Progressive exercise programs to rebuild strength and stability."},
            {"step": "4", "title": "Long-term Prevention", "desc": "Maintenance strategies and home programs to prevent recurrence."},
        ],
    },
    "sports-rehab": {
        "title": "Sports Rehabilitation",
        "subtitle": "Performance Recovery & Optimization",
        "icon": "sports_gymnastics",
        "color": "#3b82f6",
        "color_light": "rgba(59, 130, 246, 0.1)",
        "hero_desc": "Elite performance optimization and return-to-play protocols designed for professional and recreational athletes at every level.",
        "overview": "Our Sports Rehabilitation program is designed for athletes who demand peak performance. We combine sports science with clinical expertise to deliver rapid recovery from injuries, optimize performance, and prevent future setbacks. Our evidence-based protocols are tailored to your specific sport, position, and performance goals.",
        "benefits": [
            {"icon": "speed", "title": "Rapid Recovery", "desc": "Accelerated healing protocols to get you back to your sport faster and stronger."},
            {"icon": "fitness_center", "title": "Performance Enhancement", "desc": "Sport-specific conditioning and biomechanical optimization for peak performance."},
            {"icon": "shield", "title": "Injury Prevention", "desc": "Screening programs and corrective strategies to prevent common sports injuries."},
            {"icon": "psychology", "title": "Mental Conditioning", "desc": "Confidence rebuilding and mental preparation for return-to-play readiness."},
        ],
        "conditions": ["ACL/PCL Injuries", "Rotator Cuff Tears", "Tennis/Golfer's Elbow", "Ankle Sprains", "Hamstring Strains", "Stress Fractures", "Muscle Tears", "Runner's Knee"],
        "process": [
            {"step": "1", "title": "Sports-Specific Assessment", "desc": "Detailed biomechanical analysis and sport-specific functional testing."},
            {"step": "2", "title": "Targeted Intervention", "desc": "Precise treatment combining manual therapy with sport-specific rehabilitation."},
            {"step": "3", "title": "Performance Training", "desc": "Progressive loading and sport-specific drills to restore competitive readiness."},
            {"step": "4", "title": "Return-to-Play Protocol", "desc": "Structured clearance process ensuring safe and confident return to competition."},
        ],
    },
    "geriatric-care": {
        "title": "Geriatric Care",
        "subtitle": "Mobility & Independence Restoration",
        "icon": "elderly",
        "color": "#f59e0b",
        "color_light": "rgba(245, 158, 11, 0.1)",
        "hero_desc": "Compassionate mobility enhancement and strength programs designed to preserve independence and improve quality of life for seniors.",
        "overview": "Our Geriatric Care program is built on the understanding that aging doesn't mean accepting limitation. We provide gentle yet effective rehabilitation that focuses on maintaining independence, preventing falls, managing chronic conditions, and improving overall quality of life. Every program is designed with respect for the unique needs and pace of our elderly patients.",
        "benefits": [
            {"icon": "directions_walk", "title": "Fall Prevention", "desc": "Balance training and environmental modification strategies to reduce fall risk."},
            {"icon": "accessibility", "title": "Mobility Restoration", "desc": "Gentle progressive programs to improve walking ability and joint flexibility."},
            {"icon": "favorite", "title": "Chronic Pain Management", "desc": "Safe, effective techniques to manage arthritis, joint stiffness, and chronic pain."},
            {"icon": "groups", "title": "Independent Living", "desc": "Functional training to maintain daily activity independence and confidence."},
        ],
        "conditions": ["Osteoarthritis", "Osteoporosis", "Balance Disorders", "Post-Hip Replacement", "Post-Knee Replacement", "Parkinson's Disease", "Stroke Recovery", "Age-Related Muscle Loss"],
        "process": [
            {"step": "1", "title": "Gentle Assessment", "desc": "Patient, thorough evaluation of mobility, balance, strength, and daily function."},
            {"step": "2", "title": "Safe Treatment Plan", "desc": "Carefully designed program respecting individual limitations and medical history."},
            {"step": "3", "title": "Progressive Rehabilitation", "desc": "Gradual, supported exercise programs building confidence and capability."},
            {"step": "4", "title": "Home Safety & Maintenance", "desc": "Home exercise programs and safety recommendations for continued independence."},
        ],
    },
    "pain-solutions": {
        "title": "Pain Solutions",
        "subtitle": "Advanced Pain Management",
        "icon": "medical_services",
        "color": "#ef4444",
        "color_light": "rgba(239, 68, 68, 0.1)",
        "hero_desc": "Cutting-edge techniques for chronic and acute pain conditions, combining advanced manual therapy with modern modalities for lasting relief.",
        "overview": "Our Pain Solutions program takes a comprehensive, multi-modal approach to pain management. Rather than simply masking symptoms, we identify and address the underlying causes of pain through a combination of advanced manual therapy, therapeutic exercise, neuroscience education, and cutting-edge modalities. Our goal is not just relief — it's lasting resolution.",
        "benefits": [
            {"icon": "psychology", "title": "Root Cause Analysis", "desc": "Thorough diagnostic approach to identify the true source of your pain."},
            {"icon": "healing", "title": "Multi-Modal Treatment", "desc": "Combining manual therapy, dry needling, electrotherapy, and exercise for comprehensive relief."},
            {"icon": "neurology", "title": "Pain Neuroscience Education", "desc": "Understanding your pain for better self-management and faster recovery."},
            {"icon": "trending_down", "title": "Medication Reduction", "desc": "Natural pain management strategies to reduce dependence on medications."},
        ],
        "conditions": ["Chronic Back Pain", "Neck Pain", "Fibromyalgia", "Migraine & Headaches", "Neuropathic Pain", "Frozen Shoulder", "Plantar Fasciitis", "TMJ Disorders"],
        "process": [
            {"step": "1", "title": "Pain Mapping", "desc": "Detailed assessment of pain patterns, triggers, and contributing factors."},
            {"step": "2", "title": "Multi-Modal Plan", "desc": "Customized treatment combining the most effective modalities for your condition."},
            {"step": "3", "title": "Active Recovery", "desc": "Guided exercise and lifestyle modifications for sustained pain relief."},
            {"step": "4", "title": "Self-Management Mastery", "desc": "Education and tools to manage and prevent pain recurrence independently."},
        ],
    },
}

# Team data
TEAM_MEMBERS = [
    {
        "name": "Dr. Bhubon Chatterji",
        "role": "Director & Lead Specialist",
        "qualifications": "BPT, MPT (Orthopedics), 20+ Years Experience",
        "specialties": ["Spine Care", "Sports Rehab", "Manual Therapy"],
        "bio": "With over two decades of clinical excellence, Dr. Chatterji has pioneered innovative physiotherapy protocols that combine advanced manual therapy with modern tele-rehabilitation techniques.",
        "image": "/media/DOCTOR.jpeg",
        "is_lead": True,
    },
    {
        "name": "Dr. Priya Sharma",
        "role": "Senior Physiotherapist",
        "qualifications": "BPT, MPT (Neurology), 12+ Years Experience",
        "specialties": ["Geriatric Care", "Neurological Rehab"],
        "bio": "Specializing in neurological rehabilitation and geriatric care, Dr. Sharma brings compassionate expertise to every patient interaction.",
        "image": None,
        "is_lead": False,
    },
    {
        "name": "Dr. Arjun Mehta",
        "role": "Sports Rehabilitation Specialist",
        "qualifications": "BPT, CSCS, 8+ Years Experience",
        "specialties": ["Sports Rehab", "Performance Training"],
        "bio": "A certified strength and conditioning specialist, Dr. Mehta works with professional athletes to optimize recovery and peak performance.",
        "image": None,
        "is_lead": False,
    },
    {
        "name": "Dr. Sneha Patel",
        "role": "Pain Management Specialist",
        "qualifications": "BPT, MPT (Orthopedics), 10+ Years Experience",
        "specialties": ["Chronic Pain", "Dry Needling"],
        "bio": "Expert in advanced pain management techniques including dry needling, cupping therapy, and neuroscience-based pain education.",
        "image": None,
        "is_lead": False,
    },
]


def landing_page(request):
    reviews = Review.objects.filter(is_approved=True).order_by('-created_at')[:5]
    return render(request, "core/landing.html", {
        'reviews': reviews,
        'services': SERVICES,
        'force_dark': True,
        'is_home2': True,
    })


def services_page(request):
    return render(request, "core/services.html", {
        'services': SERVICES,
    })


def service_detail(request, slug):
    service = SERVICES.get(slug)
    if not service:
        from django.http import Http404
        raise Http404("Service not found")
    return render(request, "core/service_detail.html", {
        'service': service,
        'slug': slug,
        'all_services': SERVICES,
    })


def about_page(request):
    return render(request, "core/about.html", {
        'lead_doctor': TEAM_MEMBERS[0],
    })


def team_page(request):
    return render(request, "core/team.html", {
        'team_members': TEAM_MEMBERS,
    })


def contact_page(request):
    return render(request, "core/contact.html")