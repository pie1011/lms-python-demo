from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from lms_platform.core.models import UserProfile, Course, Module, Assignment, Enrollment, Submission


class Command(BaseCommand):
    help = 'Set up HR Learning & Development data with single demo employee account'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting HR Learning & Development data setup...'))

        # Create superuser
        self.create_superuser()
        
        # Create sample users with profiles
        demo_employee = self.create_sample_users()
        
        # Create sample HR training courses
        courses = self.create_sample_courses()
        
        # Create sample modules for each course
        modules = self.create_sample_modules(courses)
        
        # Create sample assignments
        assignments = self.create_sample_assignments(modules)
        
        # Create enrollments for demo employee
        enrollments = self.create_sample_enrollments(demo_employee, courses)
        
        # Create sample submissions for demo employee
        self.create_sample_submissions(demo_employee, assignments)

        self.stdout.write(
            self.style.SUCCESS('HR Learning & Development data setup completed successfully!')
        )

    def create_superuser(self):
        """Create superuser if it doesn't exist"""
        username = 'SuperKatie'
        password = 'lms-password123'
        
        if User.objects.filter(username=username).exists():
            self.stdout.write(f'Superuser "{username}" already exists.')
            return
        
        superuser = User.objects.create_superuser(
            username=username,
            email='superkatie@hrlearning.com',
            password=password,
            first_name='Super',
            last_name='Katie'
        )
        
        # Create admin UserProfile
        UserProfile.objects.create(
            user=superuser,
            role='admin',
            first_name='Super',
            last_name='Katie',
            phone_number='555-0001'
        )
        
        self.stdout.write(
            self.style.SUCCESS(f'Created superuser: {username}')
        )

    def create_sample_users(self):
        """Create sample users including ONE demo employee"""
        users_data = [
            # PRIMARY DEMO EMPLOYEE FOR PORTFOLIO
            {
                'username': 'demo_employee',
                'email': 'demo.employee@company.com',
                'first_name': 'Demo',
                'last_name': 'Employee',
                'role': 'student',
                'phone': '555-0100',
                'password': 'training123'
            },
            # STAFF USERS
            {
                'username': 'trainer1',
                'email': 'sarah.martinez@company.com',
                'first_name': 'Sarah',
                'last_name': 'Martinez',
                'role': 'instructor',
                'phone': '555-0201',
                'password': 'training123'
            },
            {
                'username': 'trainer2',
                'email': 'david.chen@company.com',
                'first_name': 'David',
                'last_name': 'Chen',
                'role': 'instructor',
                'phone': '555-0202',
                'password': 'training123'
            },
            {
                'username': 'hr_admin',
                'email': 'jennifer.brown@company.com',
                'first_name': 'Jennifer',
                'last_name': 'Brown',
                'role': 'admin',
                'phone': '555-0301',
                'password': 'training123'
            }
        ]
        
        demo_employee = None
        for user_data in users_data:
            if User.objects.filter(username=user_data['username']).exists():
                self.stdout.write(f'User "{user_data["username"]}" already exists.')
                if user_data['role'] == 'student':
                    demo_employee = User.objects.get(username=user_data['username'])
                continue
            
            user = User.objects.create_user(
                username=user_data['username'],
                email=user_data['email'],
                password=user_data['password'],
                first_name=user_data['first_name'],
                last_name=user_data['last_name']
            )
            
            UserProfile.objects.create(
                user=user,
                role=user_data['role'],
                first_name=user_data['first_name'],
                last_name=user_data['last_name'],
                phone_number=user_data['phone']
            )
            
            if user_data['role'] == 'student':
                demo_employee = user
            
            self.stdout.write(
                self.style.SUCCESS(f'Created {user_data["role"]}: {user_data["username"]}')
            )
        
        return demo_employee

    def create_sample_courses(self):
        """Create sample HR training courses"""
        courses_data = [
            {
                'course_code': 'SAFE101',
                'course_name': 'Workplace Safety Fundamentals',
                'description': 'Essential safety training covering emergency procedures, hazard identification, and workplace safety protocols. Required for all employees.',
                'credits': 2,
                'max_enrollment': 50
            },
            {
                'course_code': 'COMP201',
                'course_name': 'Compliance and Ethics Training',
                'description': 'Comprehensive training on company policies, ethical standards, anti-harassment guidelines, and regulatory compliance.',
                'credits': 3,
                'max_enrollment': 100
            },
            {
                'course_code': 'LEAD301',
                'course_name': 'Leadership Development Program',
                'description': 'Advanced leadership skills training including team management, decision-making, conflict resolution, and strategic thinking.',
                'credits': 4,
                'max_enrollment': 25
            },
            {
                'course_code': 'TECH401',
                'course_name': 'Digital Skills for Modern Workplace',
                'description': 'Technology training covering digital tools, cybersecurity awareness, data management, and productivity software.',
                'credits': 3,
                'max_enrollment': 75
            }
        ]
        
        term = 'Q1 2025'
        courses = []
        
        for course_data in courses_data:
            # Check if course already exists
            if Course.objects.filter(course_code=course_data['course_code']).exists():
                course = Course.objects.get(course_code=course_data['course_code'])
                # Update course details
                course.course_name = course_data['course_name']
                course.description = course_data['description']
                course.credits = course_data['credits']
                course.max_enrollment = course_data['max_enrollment']
                course.save()
                self.stdout.write(f'Updated course: {course}')
                courses.append(course)
                continue
            
            # Get instructor user (trainer or fallback to superuser)
            instructor = User.objects.filter(userprofile__role='instructor').first()
            if not instructor:
                instructor = User.objects.filter(is_superuser=True).first()
            
            course = Course.objects.create(
                course_code=course_data['course_code'],
                course_name=course_data['course_name'],
                description=course_data['description'],
                credits=course_data['credits'],
                term=term,
                instructor=instructor,
                max_enrollment=course_data['max_enrollment']
            )
            
            courses.append(course)
            self.stdout.write(
                self.style.SUCCESS(f'Created course: {course}')
            )
        
        return courses

    def create_sample_modules(self, courses):
        """Create sample modules for HR training courses"""
        modules_data = {
            'SAFE101': [
                {
                    'name': 'Module 1: Emergency Procedures',
                    'description': 'Learn essential emergency response procedures including evacuation routes, fire safety, and first aid basics.',
                    'content': '''
# Module 1: Emergency Procedures

## Learning Objectives
- Understand emergency evacuation procedures
- Learn fire safety protocols
- Master basic first aid techniques
- Identify emergency contact procedures

## Content Overview
This module covers critical emergency response procedures that every employee must know:

### 1. Fire Safety
- Location of fire extinguishers and exits
- Proper evacuation procedures
- Fire prevention best practices

### 2. Medical Emergencies
- When and how to call for help
- Basic first aid techniques
- AED (Automated External Defibrillator) usage

### 3. Natural Disasters
- Earthquake response procedures
- Severe weather protocols
- Shelter-in-place guidelines

### 4. Workplace Violence Prevention
- Recognition of warning signs
- De-escalation techniques
- Reporting procedures

## Assessment
Complete the emergency procedures quiz and practical scenarios to demonstrate understanding.
                    '''
                },
                {
                    'name': 'Module 2: Hazard Identification',
                    'description': 'Training on identifying and reporting workplace hazards to maintain a safe work environment.',
                    'content': '''
# Module 2: Hazard Identification and Reporting

## Learning Objectives
- Identify common workplace hazards
- Understand hazard reporting procedures
- Learn risk assessment techniques
- Practice hazard communication

## Types of Workplace Hazards
1. **Physical Hazards** - Slippery floors, electrical issues, machinery
2. **Chemical Hazards** - Cleaning supplies, laboratory chemicals
3. **Biological Hazards** - Viruses, bacteria, allergens
4. **Ergonomic Hazards** - Poor workstation setup, repetitive motions
5. **Psychosocial Hazards** - Workplace stress, harassment

## Reporting Process
Learn the proper channels for reporting hazards and the importance of immediate action.
                    '''
                }
            ],
            'COMP201': [
                {
                    'name': 'Module 1: Company Code of Conduct',
                    'description': 'Understanding company values, ethical standards, and professional behavior expectations.',
                    'content': '''
# Module 1: Company Code of Conduct

## Our Core Values
- **Integrity**: Acting with honesty and transparency
- **Respect**: Treating all individuals with dignity
- **Excellence**: Striving for quality in all we do
- **Innovation**: Embracing change and creativity
- **Collaboration**: Working together for success

## Professional Behavior Standards
Learn about expected professional conduct, communication standards, and workplace interactions.

## Ethics in Decision Making
Understand how to apply ethical principles to workplace decisions and recognize ethical dilemmas.
                    '''
                },
                {
                    'name': 'Module 2: Anti-Harassment and Discrimination',
                    'description': 'Comprehensive training on preventing harassment and discrimination in the workplace.',
                    'content': '''
# Module 2: Anti-Harassment and Discrimination

## Understanding Harassment
- Definition and types of harassment
- Recognizing inappropriate behavior
- Bystander intervention strategies

## Legal Framework
- Protected classes and characteristics
- Company policies and procedures
- Legal consequences and protections

## Reporting and Investigation Process
- How to report incidents
- Investigation procedures
- Support resources available

## Creating an Inclusive Environment
Learn how every employee contributes to a respectful and inclusive workplace.
                    '''
                }
            ]
        }
        
        modules = []
        for course in courses:
            if course.course_code in modules_data:
                for order, module_data in enumerate(modules_data[course.course_code], 1):
                    # Check if module already exists
                    if Module.objects.filter(course=course, order_number=order).exists():
                        module = Module.objects.get(course=course, order_number=order)
                        module.module_name = module_data['name']
                        module.description = module_data['description']
                        module.content = module_data['content']
                        module.save()
                        self.stdout.write(f'Updated module: {module.module_name}')
                        modules.append(module)
                        continue
                    
                    module = Module.objects.create(
                        course=course,
                        module_name=module_data['name'],
                        description=module_data['description'],
                        order_number=order,
                        content=module_data['content']
                    )
                    
                    modules.append(module)
                    self.stdout.write(
                        self.style.SUCCESS(f'Created module: {module.module_name}')
                    )
        
        return modules

    def create_sample_assignments(self, modules):
        """Create sample assignments for HR training modules"""
        assignments = []
        
        for module in modules:
            if 'Emergency Procedures' in module.module_name:
                assignment_name = 'Emergency Response Knowledge Check'
                description = 'Assessment covering emergency procedures, evacuation routes, and first aid protocols.'
                instructions = '''
Complete this knowledge check to demonstrate your understanding of emergency procedures:

**Part A: Multiple Choice Questions (50 points)**
1. What is the first step during a fire emergency?
2. Where are the nearest fire extinguishers located?
3. What number do you call for medical emergencies?

**Part B: Scenario Analysis (30 points)**
Read the following scenarios and describe the appropriate response:
- Scenario 1: You notice smoke coming from an electrical panel
- Scenario 2: A colleague has fallen and appears injured
- Scenario 3: You hear the tornado warning siren

**Part C: Practical Knowledge (20 points)**
1. Draw a map showing evacuation routes from your work area
2. List the contents of a basic first aid kit
3. Explain when to use an AED

**Submission Requirements:**
- Complete all sections thoroughly
- Show your work and reasoning
- Submit within 48 hours of module completion
                '''
                assignment_type = 'quiz'
                max_points = 100
                
            elif 'Hazard Identification' in module.module_name:
                assignment_name = 'Workplace Hazard Assessment'
                description = 'Practical exercise identifying and documenting potential workplace hazards.'
                instructions = '''
Conduct a hazard assessment of your immediate work area:

**Assignment Tasks:**
1. **Hazard Identification (40 points)**
   - Walk through your workspace
   - Identify at least 5 potential hazards
   - Categorize each hazard (physical, chemical, biological, ergonomic, psychosocial)

2. **Risk Assessment (30 points)**
   - Rate each hazard's likelihood (Low/Medium/High)
   - Rate each hazard's severity (Low/Medium/High)
   - Prioritize hazards based on risk level

3. **Corrective Actions (30 points)**
   - Propose solutions for each identified hazard
   - Indicate whether action is immediate or long-term
   - Identify who should be responsible for corrections

**Deliverable:** Submit a completed Hazard Assessment Form with photos if appropriate.
                '''
                assignment_type = 'project'
                max_points = 100
                
            elif 'Code of Conduct' in module.module_name:
                assignment_name = 'Ethics Case Study Analysis'
                description = 'Analyze workplace scenarios and apply company ethical standards.'
                instructions = '''
Review the following case studies and provide your analysis:

**Case Study 1: Conflict of Interest**
An employee's spouse owns a company that could be a potential vendor. The employee is on the vendor selection committee.

**Case Study 2: Confidential Information**
You overhear confidential information about layoffs. A friend asks if their job is safe.

**Case Study 3: Gift Policy**
A client offers expensive tickets to a sporting event as appreciation for your service.

**For Each Case Study:**
1. Identify the ethical issue(s)
2. Reference relevant company policies
3. Recommend appropriate action
4. Explain your reasoning

**Requirements:**
- 2-3 paragraphs per case study
- Cite specific policy sections
- Professional writing style
                '''
                assignment_type = 'homework'
                max_points = 75
                
            elif 'Anti-Harassment' in module.module_name:
                assignment_name = 'Bystander Intervention Scenarios'
                description = 'Practice recognizing and responding to inappropriate workplace behavior.'
                instructions = '''
Complete the interactive scenarios demonstrating bystander intervention skills:

**Scenario-Based Questions:**
You will be presented with 5 workplace situations involving potentially inappropriate behavior.

**For Each Scenario:**
1. Identify what behavior is concerning
2. Determine if intervention is appropriate
3. Choose the best intervention strategy
4. Explain potential next steps

**Response Options May Include:**
- Direct intervention
- Distraction technique
- Delegate to authority
- Document and report
- Support the target afterward

**Assessment Criteria:**
- Accurate identification of inappropriate behavior
- Appropriate intervention strategy selection
- Understanding of reporting procedures
- Demonstration of support for affected individuals

This is a critical skill for maintaining a respectful workplace environment.
                '''
                assignment_type = 'exam'
                max_points = 100
                
            else:
                # Default assignment for other modules
                assignment_name = f'{module.module_name} Completion Quiz'
                description = f'Knowledge assessment for {module.module_name}'
                instructions = '''
Complete the quiz covering key concepts from this training module.

**Instructions:**
- Read each question carefully
- Select the best answer for multiple choice questions
- Provide complete responses for short answer questions
- You have 60 minutes to complete the quiz
- A passing score is 80% or higher

**Topics Covered:**
- Key learning objectives from the module
- Practical application scenarios
- Company policy and procedure knowledge
- Best practices and recommendations

Good luck!
                '''
                assignment_type = 'quiz'
                max_points = 50
            
            # Check if assignment already exists
            if Assignment.objects.filter(module=module, assignment_name=assignment_name).exists():
                assignment = Assignment.objects.get(module=module, assignment_name=assignment_name)
                assignment.description = description
                assignment.instructions = instructions
                assignment.assignment_type = assignment_type
                assignment.max_points = max_points
                assignment.save()
                self.stdout.write(f'Updated assignment: {assignment_name}')
                assignments.append(assignment)
                continue
            
            # Set due date to 2 weeks from now
            due_date = timezone.now() + timedelta(days=14)
            
            assignment = Assignment.objects.create(
                module=module,
                assignment_name=assignment_name,
                description=description,
                due_date=due_date,
                max_points=max_points,
                assignment_type=assignment_type,
                instructions=instructions
            )
            
            assignments.append(assignment)
            self.stdout.write(
                self.style.SUCCESS(f'Created assignment: {assignment_name}')
            )
        
        return assignments

    def create_sample_enrollments(self, demo_employee, courses):
        """Create sample enrollments for demo employee"""
        if not demo_employee:
            self.stdout.write(self.style.ERROR('No demo employee found! Cannot create enrollments.'))
            return []
        
        enrollments = []
        
        # Enroll demo employee in first two courses (Safety and Compliance - typical required training)
        required_courses = courses[:2]  # SAFE101 and COMP201
        
        for course in required_courses:
            # Check if enrollment already exists
            if Enrollment.objects.filter(student=demo_employee, course=course).exists():
                enrollment = Enrollment.objects.get(student=demo_employee, course=course)
                self.stdout.write(f'Enrollment for {demo_employee.username} in {course.course_code} already exists.')
                enrollments.append(enrollment)
                continue
            
            enrollment = Enrollment.objects.create(
                student=demo_employee,
                course=course,
                current_grade=None,  # Will be calculated from submissions
                status='active'
            )
            
            enrollments.append(enrollment)
            self.stdout.write(
                self.style.SUCCESS(f'Created enrollment: {demo_employee.username} in {course.course_code}')
            )
        
        return enrollments

    def create_sample_submissions(self, demo_employee, assignments):
        """Create sample submissions for demo employee"""
        if not demo_employee:
            self.stdout.write(self.style.ERROR('No demo employee found! Cannot create submissions.'))
            return
        
        # Create submissions for first few assignments to show progress
        for assignment in assignments[:2]:  # Submit to first 2 assignments
            # Check if submission already exists
            if Submission.objects.filter(student=demo_employee, assignment=assignment).exists():
                self.stdout.write(f'Submission for {demo_employee.username} on {assignment.assignment_name} already exists.')
                continue
            
            if 'Emergency Response' in assignment.assignment_name:
                submission_content = '''
**Part A: Multiple Choice Answers**
1. A) Activate the fire alarm and evacuate immediately
2. B) Located on each floor near the main exits and in the break room
3. C) 911 for all medical emergencies

**Part B: Scenario Analysis**
Scenario 1: I would immediately report the smoke to security and evacuate the area. I would not attempt to investigate or touch the electrical panel.

Scenario 2: I would check if the person is conscious and breathing. If they are seriously injured, I would call 911 immediately and not move them. I would provide comfort and basic first aid if trained to do so.

Scenario 3: I would immediately go to the designated shelter area (interior hallway on the ground floor) and stay away from windows until the all-clear signal.

**Part C: Practical Knowledge**
1. [Evacuation map drawing would be included here]
2. First aid kit contents: bandages, antiseptic wipes, pain relievers, emergency contact list, instant cold pack, gloves
3. AED should be used when someone is unconscious and not breathing normally. Call 911 first, then follow the AED voice prompts.
                '''
                grade = 92.0
                feedback = 'Excellent work! You demonstrated a clear understanding of emergency procedures. Your scenario responses show good judgment and prioritization of safety. The evacuation route drawing was accurate and well-labeled.'
                
            elif 'Hazard Assessment' in assignment.assignment_name:
                submission_content = '''
**Hazard Assessment Report - Workstation Area**

**Identified Hazards:**
1. **Electrical cables across walkway** (Physical) - High likelihood, Medium severity
2. **Poor lighting at desk** (Ergonomic) - Medium likelihood, Low severity  
3. **Heavy boxes stored on high shelf** (Physical) - Low likelihood, High severity
4. **Cluttered emergency exit path** (Physical) - Medium likelihood, High severity
5. **No hand sanitizer available** (Biological) - High likelihood, Low severity

**Risk Prioritization:**
1. Cluttered emergency exit (High risk)
2. Heavy boxes on high shelf (Medium risk)  
3. Electrical cables (Medium risk)
4. Poor lighting (Low risk)
5. Hand sanitizer (Low risk)

**Corrective Actions:**
1. Immediate: Clear exit path and establish maintenance schedule
2. Long-term: Install proper shelving and weight limits
3. Immediate: Secure cables with cord management
4. Long-term: Request additional desk lighting
5. Immediate: Request hand sanitizer station
                '''
                grade = 88.0
                feedback = 'Good hazard identification and risk assessment! You correctly prioritized the emergency exit issue. Consider including more details about who to contact for each corrective action.'
                
            else:
                # Default submission for other assignments
                submission_content = '''
I have completed the training module and reviewed all materials thoroughly. 

Key takeaways from this training:
- Understanding of company policies and procedures
- Importance of maintaining professional standards
- Recognition of my role in creating a positive workplace environment
- Knowledge of proper reporting procedures when issues arise

I feel confident in applying these concepts to my daily work and will reference the training materials as needed. Thank you for providing this important professional development opportunity.
                '''
                grade = 85.0
                feedback = 'Good completion of the training requirements. Your responses demonstrate understanding of the key concepts. Continue to apply these principles in your daily work.'
            
            submission = Submission.objects.create(
                student=demo_employee,
                assignment=assignment,
                submission_content=submission_content,
                grade=grade,
                feedback=feedback,
                graded_by=assignment.module.course.instructor,
                graded_at=timezone.now(),
                status='graded'
            )
            
            self.stdout.write(
                self.style.SUCCESS(f'Created submission: {demo_employee.username} - {assignment.assignment_name}')
            )