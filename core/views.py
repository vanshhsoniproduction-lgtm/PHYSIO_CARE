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
        "overview": "Our Spine & Disc Care program combines advanced manual therapy techniques with evidence-based rehabilitation protocols to address the root cause of spinal disorders. With over 22 years of specialization, Dr. Bhubon Chatterji has developed proprietary treatment methodologies that have helped thousands of patients avoid surgery and regain their quality of life.",
        "benefits": [
            {"icon": "healing", "title": "Non-Surgical Solutions", "desc": "Advanced conservative treatments that address disc herniations and spinal stenosis without surgery."},
            {"icon": "straighten", "title": "Posture Correction", "desc": "Comprehensive postural assessment and correction programs for long-term spinal health."},
            {"icon": "self_improvement", "title": "Core Stabilization", "desc": "Targeted strengthening protocols to build a natural spinal support system."},
            {"icon": "monitor_heart", "title": "Pain Management", "desc": "Multi-modal pain relief strategies combining manual therapy, electrotherapy, and exercise."},
        ],
        "conditions": [
            "Cervical Spondylosis",
            "Cervical Disc Bulge",
            "Cervical Disc Herniation (Slipped Disc)",
            "Cervical Radiculopathy (Pinched Nerve)",
            "Facet Joint Syndrome",
            "Whiplash Injury",
            "Cervicogenic Headache",
            "Text Neck Syndrome",
            "Torticollis (Wry Neck)",
            "Thoracic Facet Joint Dysfunction",
            "Thoracic Kyphosis",
            "Costovertebral Joint Dysfunction",
            "Thoracic Muscle Strain",
            "Scheuermann's Disease",
            "Lumbar Disc Bulge",
            "Lumbar Radiculopathy",
            "Sciatica",
            "Degenerative Disc Disease (DDD)",
            "Lumbar Spondylosis",
            "Lumbar Muscle Strain",
            "Sacroiliac (SI) Joint Dysfunction",
            "Lumbar Spinal Stenosis",
            "Spondylolisthesis",
            "Spondylolysis",
            "Mechanical Low Back Pain",
            "Upper cross syndrome",
            "Lower cross syndrome",
            "Annular Tear (Annular Fissure)",
            "Disc Desiccation (Disc Dehydration)",
            "Pinched Nerve",
            "Stress Fracture of the Spine (Spondylolysis)",
            "Pars Interarticularis Injury",
            "Hyperextension Injury",
            "Compression Fracture",
            "Coccydynia"
        ],
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
        "conditions": [
            "Meniscal injury",
            "LCL/MCL injury",
            "Jumpers knee",
            "Osgood schlatters disease",
            "ATFL injury",
            "CFL injury",
            "Achilles tendinitis",
            "Stress fracture",
            "Ankle instability",
            "Quadriceps strain",
            "Muscle strain",
            "Ligament tear",
            "Shin splint",
            "Hamstring tendinitis",
            "IT band syndrome",
            "Golfer’s elbow",
            "TFCC injury",
            "Wrist sprain",
            "UCL injury",
            "Shoulder impingement syndrome",
            "AC joint strain",
            "SLAP lesion",
            "Hill Sachs lesion",
            "Whiplash injury"
        ],
        "athletes": [
            "Golfer",
            "Cricketer",
            "Footballer",
            "Basketball player",
            "Runner (Sprinter/Middle-distance/Marathon)",
            "Swimmer",
            "MMA Fighter",
            "Wrestler",
            "Tennis Player",
            "Squash Player",
            "Polo Player",
            "Pickleball Player",
            "Equestrian Rider",
            "Hockey Player",
            "Badminton Player",
            "Volleyball Player",
            "Rugby Player",
            "Baseball Player",
            "Table Tennis Player",
            "Archer",
            "Boxer",
            "Cyclist",
            "Gymnast",
            "Weightlifter",
            "Powerlifter"
        ],
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
        "conditions": [
            "Osteoarthritis (Knee, Hip, Shoulder)",
            "Osteoporosis",
            "Osteopenia",
            "Rheumatoid Arthritis",
            "Frozen Shoulder (Adhesive Capsulitis)",
            "Degenerative Joint Disease (DJD)",
            "Balance Disorders",
            "Pathological gait",
            "Gait Instability",
            "Chronic Low Back Pain",
            "Vertebral Compression Fractures",
            "Sarcopenia (Age-related Muscle Loss)",
            "General Muscle Weakness",
            "Mobility Limitations",
            "Joint stiffness",
            "Plantar fasciitis",
            "Calcaneal spur (heel pain)",
            "Bursitis",
            "Pes anserinus",
            "Retro Calcaneal bursitis",
            "Total Knee Replacement (TKR)",
            "Total Hip Replacement (THR)",
            "Fracture Rehabilitation",
            "Shoulder Dislocation Rehabilitation"
        ],
        "process": [
            {"step": "1", "title": "Gentle Assessment", "desc": "Patient, thorough evaluation of mobility, balance, strength, and daily function."},
            {"step": "2", "title": "Safe Treatment Plan", "desc": "Carefully designed program respecting individual limitations and medical history."},
            {"step": "3", "title": "Progressive Rehabilitation", "desc": "Gradual, supported exercise programs building confidence and capability."},
            {"step": "4", "title": "Home Safety & Maintenance", "desc": "Home exercise programs and safety recommendations for continued independence."},
        ],
    },
    "neuro-care": {
        "title": "Neurological Rehabilitation",
        "subtitle": "Neuro Restoration & Functional Recovery",
        "icon": "psychology",
        "color": "#10b981",
        "color_light": "rgba(16, 185, 129, 0.1)",
        "hero_desc": "Specialized neuro-rehabilitation programs to restore motor function, enhance neuroplasticity, and improve independence for neurological conditions.",
        "overview": "Our Neurological Rehabilitation program is designed to help individuals recover from neurological disorders, stroke, and nerve injuries. Leveraging advanced neurodevelopmental treatment (NDT/Bobath) and motor learning principles, we aim to stimulate neuroplasticity, restore lost functions, and help our patients regain maximum independence and confidence in their daily lives.",
        "benefits": [
            {"icon": "psychology", "title": "Neuroplasticity Stimulation", "desc": "Targeted therapies designed to rebuild neural pathways and restore motor control."},
            {"icon": "balance", "title": "Balance & Gait Training", "desc": "Advanced protocols to improve equilibrium, prevent falls, and restore natural gait patterns."},
            {"icon": "edit_note", "title": "Fine Motor Recovery", "desc": "Specialized hand and upper limb rehabilitation for dexterity and coordination."},
            {"icon": "fitness_center", "title": "Spasticity Management", "desc": "Therapeutic exercises to reduce muscle stiffness and improve functional strength."},
        ],
        "conditions": [
            "Stroke Rehabilitation",
            "Parkinson’s Disease",
            "Bell’s palsy",
            "Facial nerve palsy",
            "Peripheral Neuropathy",
            "Wrist drop",
            "Foot drop",
            "Spinal Cord Injury Rehabilitation",
            "Guillain-Barré Syndrome (GBS)",
            "Multiple Sclerosis",
            "Motor Neuron Disease (MND)",
            "Cerebellar Ataxia",
            "Balance & Vestibular Disorders"
        ],
        "process": [
            {"step": "1", "title": "Detailed Neuro Assessment", "desc": "Comprehensive evaluation of reflexes, muscle tone, balance, gait, and functional independence."},
            {"step": "2", "title": "Goal-Oriented Planning", "desc": "Designing a customized treatment plan targeting specific functional goals (walking, writing, self-care)."},
            {"step": "3", "title": "Neurodevelopmental Therapy", "desc": "Hands-on therapy incorporating motor learning, sensory stimulation, and task-specific training."},
            {"step": "4", "title": "Family Training & Home Program", "desc": "Equipping caregivers and establishing a home environment that supports ongoing recovery."},
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
        "qualifications": "BPT, MPT (Orthopedics), 22+ Years Experience",
        "specialties": ["Spine Care", "Sports Rehab", "Manual Therapy"],
        "bio": "With over 22 years of clinical excellence, Dr. Chatterji has pioneered innovative physiotherapy protocols that combine advanced manual therapy with modern tele-rehabilitation techniques.",
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
        'bg_frames_path': '/media/frames/bg_home',
        'bg_frames_count': 80,
    })


def services_page(request):
    return render(request, "core/services.html", {
        'services': SERVICES,
        'force_dark': True,
        'is_home2': True,
        'bg_video_url': '/media/bg_contact.mp4',
        'bg_frames_path': '/media/frames/bg_contact',
        'bg_frames_count': 80,
    })


def service_detail(request, slug):
    service = SERVICES.get(slug)
    if not service:
        from django.http import Http404
        raise Http404("Service not found")
    
    context = {
        'service': service,
        'slug': slug,
        'all_services': SERVICES,
        'force_dark': True,
        'is_home2': True,
        'bg_frames_path': '/media/frames/bg_home',
        'bg_frames_count': 80,
    }
    
    if slug == 'sports-rehab':
        context['bg_video_url'] = '/media/bg_service2.mp4'
        context['bg_frames_path'] = '/media/frames/bg_service2'
        
    return render(request, "core/service_detail.html", context)


def about_page(request):
    return render(request, "core/about.html", {
        'lead_doctor': TEAM_MEMBERS[0],
        'force_dark': True,
        'is_home2': True,
        'bg_frames_path': '/media/frames/bg_home',
        'bg_frames_count': 80,
    })


def team_page(request):
    return render(request, "core/team.html", {
        'team_members': TEAM_MEMBERS,
        'force_dark': True,
        'is_home2': True,
        'bg_frames_path': '/media/frames/bg_home',
        'bg_frames_count': 80,
    })


def contact_page(request):
    return render(request, "core/contact.html", {
        'force_dark': True,
        'is_home2': True,
        'bg_video_url': '/media/bg_contact.mp4',
        'bg_frames_path': '/media/frames/bg_contact',
        'bg_frames_count': 80,
    })