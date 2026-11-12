import os
from datetime import datetime, timedelta, timezone
from werkzeug.security import generate_password_hash
from app import app, db, User, Event, Registration, Venue, Speaker, Sponsorship, Incident, Notification, Reminder, Feedback

def seed():
    with app.app_context():
        print("🌱 Seeding database with comprehensive user and admin data...")
        db.create_all()

        now = datetime.now(timezone.utc)

        # ---------------- 1. USERS ----------------
        users_data = [
            {'name': 'Admin User', 'email': 'admin@eventops.com', 'role': 'admin', 'pass': 'admin123'},
            {'name': 'Elena Vance (Ops Lead)', 'email': 'director@eventops.com', 'role': 'admin', 'pass': 'admin123'},
            {'name': 'Alex Mercer', 'email': 'user@eventops.com', 'role': 'user', 'pass': 'user123'},
            {'name': 'Sarah Jenkins', 'email': 'sarah.jenkins@techcorp.io', 'role': 'user', 'pass': 'user123'},
            {'name': 'David Chen', 'email': 'david.chen@innovate.org', 'role': 'user', 'pass': 'user123'},
            {'name': 'Priya Sharma', 'email': 'priya.sharma@cloudsummit.com', 'role': 'user', 'pass': 'user123'},
            {'name': 'Marcus Brooks', 'email': 'marcus.brooks@fintechhub.net', 'role': 'user', 'pass': 'user123'}
        ]

        user_map = {}
        for u in users_data:
            existing = User.query.filter_by(email=u['email']).first()
            if not existing:
                user = User(
                    name=u['name'],
                    email=u['email'],
                    role=u['role'],
                    created_at=now - timedelta(days=60)
                )
                user.set_password(u['pass'])
                db.session.add(user)
                db.session.commit()
                user_map[u['email']] = user
                print(f"  + Added user: {u['email']} ({u['role']})")
            else:
                existing.name = u['name']
                existing.role = u['role']
                existing.set_password(u['pass'])
                db.session.commit()
                user_map[u['email']] = existing
                print(f"  * Updated user: {u['email']} ({u['role']})")

        # ---------------- 2. EVENTS ----------------
        events_data = [
            {
                'id': 1,
                'title': 'AI Summit 2026: Autonomous Agents & LLMs',
                'description': 'The premier global summit bringing together AI researchers, systems architects, and engineering leaders to explore multi-agent architectures, real-time reasoning, and production deployments.',
                'date': '2026-07-10',
                'time': '09:00 AM',
                'location': 'Main Grand Auditorium',
                'capacity': 350,
                'status': 'upcoming'
            },
            {
                'id': 2,
                'title': 'Cloud Native & Kubernetes Hackathon',
                'description': '24-hour hands-on coding challenge building scalable microservices, zero-trust security mesh networks, and automated incident recovery engines.',
                'date': '2026-07-15',
                'time': '06:00 PM',
                'location': 'Silicon Hall Alpha',
                'capacity': 150,
                'status': 'upcoming'
            },
            {
                'id': 3,
                'title': 'Global FinTech & Digital Economy Expo',
                'description': 'High-profile expo covering algorithmic liquidity, decentralized real-time settlement rails, AI credit scoring, and open banking API compliance.',
                'date': '2026-07-22',
                'time': '10:00 AM',
                'location': 'Exhibition Pavilion',
                'capacity': 300,
                'status': 'upcoming'
            },
            {
                'id': 4,
                'title': 'CyberSec Defense & Threat Intelligence Forum',
                'description': 'Deep-dive security symposium focusing on LLM-assisted vulnerability identification, automated penetration testing, and zero-day threat surface isolation.',
                'date': '2026-08-05',
                'time': '08:30 AM',
                'location': 'Quantum Lab Suite',
                'capacity': 180,
                'status': 'upcoming'
            },
            {
                'id': 5,
                'title': 'Sponsor & Executive Partner Reception',
                'description': 'Exclusive private networking lounge and strategic roundtable connecting enterprise sponsors, venture partners, and key platform contributors.',
                'date': '2026-08-12',
                'time': '06:30 PM',
                'location': 'VIP Emerald Lounge',
                'capacity': 80,
                'status': 'upcoming'
            },
            {
                'id': 6,
                'title': 'Product Design & Generative UI Masterclass',
                'description': 'Interactive workshop dissecting adaptive interfaces, dynamic component synthesis, token-driven theming, and multi-modal UX patterns.',
                'date': '2026-08-20',
                'time': '02:00 PM',
                'location': 'Workshop Studio B',
                'capacity': 60,
                'status': 'upcoming'
            },
            {
                'id': 7,
                'title': 'Spring Developers Kickoff 2026',
                'description': 'Community gathering celebrating open source milestones, showcasing ecosystem integrations, and awarding developer bounties.',
                'date': '2026-04-10',
                'time': '09:30 AM',
                'location': 'Main Grand Auditorium',
                'capacity': 400,
                'status': 'completed'
            },
            {
                'id': 8,
                'title': 'DevOps & SRE Live Arena 2026',
                'description': 'Full day of continuous delivery simulations, chaos testing exercises, and automated telemetry post-mortem reviews.',
                'date': '2026-11-02',
                'time': '10:00 AM',
                'location': 'Room B',
                'capacity': 120,
                'status': 'ongoing'
            }
        ]

        event_map = {}
        for ed in events_data:
            ev = Event.query.get(ed['id'])
            if not ev:
                ev = Event(
                    id=ed['id'],
                    title=ed['title'],
                    description=ed['description'],
                    date=ed['date'],
                    time=ed['time'],
                    location=ed['location'],
                    capacity=ed['capacity'],
                    status=ed['status'],
                    created_at=now - timedelta(days=40)
                )
                db.session.add(ev)
                print(f"  + Added event: {ed['title']}")
            else:
                ev.title = ed['title']
                ev.description = ed['description']
                ev.date = ed['date']
                ev.time = ed['time']
                ev.location = ed['location']
                ev.capacity = ed['capacity']
                ev.status = ed['status']
                print(f"  * Updated event: {ed['title']}")
            db.session.commit()
            event_map[ed['id']] = ev

        # ---------------- 3. VENUES ----------------
        venues_data = [
            {'name': 'Main Grand Auditorium', 'capacity': 450, 'utilization': 0.82, 'status': 'available'},
            {'name': 'Silicon Hall Alpha', 'capacity': 200, 'utilization': 0.65, 'status': 'available'},
            {'name': 'Exhibition Pavilion', 'capacity': 350, 'utilization': 0.88, 'status': 'booked'},
            {'name': 'Quantum Lab Suite', 'capacity': 180, 'utilization': 0.40, 'status': 'available'},
            {'name': 'Room B', 'capacity': 120, 'utilization': 0.75, 'status': 'available'},
            {'name': 'VIP Emerald Lounge', 'capacity': 80, 'utilization': 0.30, 'status': 'available'},
            {'name': 'Workshop Studio B', 'capacity': 60, 'utilization': 0.70, 'status': 'available'},
        ]
        for vd in venues_data:
            existing_v = Venue.query.filter_by(name=vd['name']).first()
            if not existing_v:
                v = Venue(name=vd['name'], capacity=vd['capacity'], utilization=vd['utilization'], status=vd['status'])
                db.session.add(v)
            else:
                existing_v.capacity = vd['capacity']
                existing_v.utilization = vd['utilization']
                existing_v.status = vd['status']
        db.session.commit()
        print("  + Venues synchronized.")

        # ---------------- 4. SPEAKERS ----------------
        speakers_data = [
            {
                'name': 'Dr. Aris Thorne',
                'bio': 'Chief AI Scientist at NeuralCore. Pioneer in reinforcement learning and collaborative autonomous agent architectures.',
                'session_title': 'Keynote: Multi-Agent Production Workflows in Enterprise',
                'schedule': 'Day 1 09:30 AM',
                'availability': True
            },
            {
                'name': 'Sophia Sterling',
                'bio': 'VP of Cloud Engineering at ScaleStream. Former principal architect specializing in zero-trust mesh infrastructure.',
                'session_title': 'Zero-Trust Service Meshes & Ephemeral Containers',
                'schedule': 'Day 1 11:30 AM',
                'availability': True
            },
            {
                'name': 'Liam O\'Connor',
                'bio': 'Principal Threat Researcher at DefSec Labs. Author of foundational papers on proactive zero-day surface isolation.',
                'session_title': 'Autonomous Threat Hunting using Deep Transformer Models',
                'schedule': 'Day 1 02:30 PM',
                'availability': True
            },
            {
                'name': 'Maya Patel',
                'bio': 'Lead Financial Systems Architect at ApexPay. Specializes in sub-millisecond liquidity protocols and cross-chain settlement.',
                'session_title': 'Decentralized Liquidity & Instant Real-Time Settlement',
                'schedule': 'Day 2 10:00 AM',
                'availability': True
            },
            {
                'name': 'Marcus Holloway',
                'bio': 'Director of Reliability Engineering at HyperScale. 15 years operating mission-critical distributed databases.',
                'session_title': 'Post-Mortem: Surviving Black Swan Distributed Outages',
                'schedule': 'Day 2 01:30 PM',
                'availability': True
            },
            {
                'name': 'Elena Vasquez',
                'bio': 'Head of Design Systems at InterfaceLabs. Pioneer in human-centered AI and generative interface paradigms.',
                'session_title': 'Generative UI: Dynamic Interfaces Synthesized in Real Time',
                'schedule': 'Day 2 03:30 PM',
                'availability': True
            }
        ]
        for sd in speakers_data:
            existing_s = Speaker.query.filter_by(name=sd['name']).first()
            if not existing_s:
                spk = Speaker(
                    name=sd['name'],
                    bio=sd['bio'],
                    session_title=sd['session_title'],
                    schedule=sd['schedule'],
                    availability=sd['availability']
                )
                db.session.add(spk)
            else:
                existing_s.bio = sd['bio']
                existing_s.session_title = sd['session_title']
                existing_s.schedule = sd['schedule']
                existing_s.availability = sd['availability']
        db.session.commit()
        print("  + Speakers synchronized.")

        # ---------------- 5. SPONSORSHIPS ----------------
        sponsorships_data = [
            {
                'sponsor_name': 'Google Cloud',
                'commitment': '$100,000 (Titanium)',
                'deliverables': 'Keynote Stage Naming, VIP Dinner Sponsor, 400 sq ft Exhibition Booth, Live Telemetry Stream',
                'visibility_score': 95,
                'roi': 1.85
            },
            {
                'sponsor_name': 'Stripe',
                'commitment': '$65,000 (Platinum)',
                'deliverables': 'Hackathon Track Sponsor, Main Lanyard Branding, Developer Lounge & Lightning Talks',
                'visibility_score': 90,
                'roi': 1.50
            },
            {
                'sponsor_name': 'Datadog',
                'commitment': '$45,000 (Gold)',
                'deliverables': 'Observability Workshop Booth, Digital Signage Promos, Swag Bag Inserts, Tech Blog Feature',
                'visibility_score': 84,
                'roi': 1.35
            },
            {
                'sponsor_name': 'GitHub',
                'commitment': '$35,000 (Gold)',
                'deliverables': 'Hackathon Code Repository Sponsor, Coffee Station Host, Official Badge Sponsor',
                'visibility_score': 80,
                'roi': 1.25
            },
            {
                'sponsor_name': 'Cloudflare',
                'commitment': '$25,000 (Silver)',
                'deliverables': 'Attendee Wi-Fi Portal Branding, Breakout Session Sponsor, Digital Program Ad',
                'visibility_score': 72,
                'roi': 1.10
            },
            {
                'sponsor_name': 'Vercel',
                'commitment': '$15,000 (Community)',
                'deliverables': 'Speaker Green Room Sponsor, Community Showcase Demo, Swag Contribution',
                'visibility_score': 68,
                'roi': 0.95
            }
        ]
        for spd in sponsorships_data:
            existing_sp = Sponsorship.query.filter_by(sponsor_name=spd['sponsor_name']).first()
            if not existing_sp:
                sp = Sponsorship(
                    sponsor_name=spd['sponsor_name'],
                    commitment=spd['commitment'],
                    deliverables=spd['deliverables'],
                    visibility_score=spd['visibility_score'],
                    roi=spd['roi']
                )
                db.session.add(sp)
            else:
                existing_sp.commitment = spd['commitment']
                existing_sp.deliverables = spd['deliverables']
                existing_sp.visibility_score = spd['visibility_score']
                existing_sp.roi = spd['roi']
        db.session.commit()
        print("  + Sponsorships synchronized.")

        # ---------------- 6. INCIDENTS ----------------
        incidents_data = [
            {
                'title': 'Wi-Fi 5GHz Channel Congestion in Main Hall',
                'description': 'High attendee density caused temporary 12% packet drops on access points 12-16 during opening keynote. Additional high-capacity APs deployed and spectrum load rebalanced.',
                'priority': 'high',
                'status': 'resolved',
                'reported_at': now - timedelta(hours=3),
                'resolved_at': now - timedelta(hours=1, minutes=45)
            },
            {
                'title': 'Registration Kiosk #3 Thermal Paper Ribbon Depleted',
                'description': 'Badge printing kiosk 3 ran out of heavy cardstock thermal ribbon. Ribbon restocked and test print verification passed.',
                'priority': 'medium',
                'status': 'resolved',
                'reported_at': now - timedelta(hours=5),
                'resolved_at': now - timedelta(hours=4, minutes=40)
            },
            {
                'title': 'Audio Feedback Loop on Stage Lavalier Mic #2',
                'description': '4kHz acoustic resonance detected when speaker steps near front-of-house fills. AV engineer applying narrow notch equalization filter.',
                'priority': 'medium',
                'status': 'open',
                'reported_at': now - timedelta(minutes=25),
                'resolved_at': None
            },
            {
                'title': 'Catering Coffee Urn Depleted at Station B',
                'description': 'Morning coffee urn in north concourse emptied before scheduled break. Catering staff delivered 2 fresh 10-gallon urns.',
                'priority': 'low',
                'status': 'resolved',
                'reported_at': now - timedelta(hours=2),
                'resolved_at': now - timedelta(hours=1, minutes=30)
            },
            {
                'title': 'Wayfinding Digital Screen #4 Intermittent Sync Loss',
                'description': 'Left vertical display in registration foyer experiencing periodic HDMI handshake loss. Replacement active optical cable staged for inter-session swap.',
                'priority': 'low',
                'status': 'open',
                'reported_at': now - timedelta(minutes=15),
                'resolved_at': None
            }
        ]
        for incd in incidents_data:
            existing_inc = Incident.query.filter_by(title=incd['title']).first()
            if not existing_inc:
                inc = Incident(
                    title=incd['title'],
                    description=incd['description'],
                    priority=incd['priority'],
                    status=incd['status'],
                    reported_at=incd['reported_at'],
                    resolved_at=incd['resolved_at']
                )
                db.session.add(inc)
        db.session.commit()
        print("  + Incidents synchronized.")

        # ---------------- 7. REGISTRATIONS ----------------
        u_alex = user_map.get('user@eventops.com')
        u_admin = user_map.get('admin@eventops.com')
        u_sarah = user_map.get('sarah.jenkins@techcorp.io')
        u_david = user_map.get('david.chen@innovate.org')
        u_priya = user_map.get('priya.sharma@cloudsummit.com')
        u_marcus = user_map.get('marcus.brooks@fintechhub.net')

        # Ensure registrations for main test users
        regs_seed = [
            # Alex Mercer (regular user): 4 registrations
            {'user': u_alex, 'event_id': 1, 'ticket': 'VIP', 'checked_in': True, 'status': 'registered'},
            {'user': u_alex, 'event_id': 2, 'ticket': 'Standard', 'checked_in': True, 'status': 'registered'},
            {'user': u_alex, 'event_id': 3, 'ticket': 'VIP', 'checked_in': False, 'status': 'registered'},
            {'user': u_alex, 'event_id': 4, 'ticket': 'Standard', 'checked_in': False, 'status': 'registered'},
            # Admin User: 3 registrations
            {'user': u_admin, 'event_id': 1, 'ticket': 'Speaker', 'checked_in': True, 'status': 'registered'},
            {'user': u_admin, 'event_id': 5, 'ticket': 'VIP', 'checked_in': False, 'status': 'registered'},
            {'user': u_admin, 'event_id': 7, 'ticket': 'Standard', 'checked_in': True, 'status': 'registered'},
            # Other users
            {'user': u_sarah, 'event_id': 1, 'ticket': 'VIP', 'checked_in': True, 'status': 'registered'},
            {'user': u_sarah, 'event_id': 3, 'ticket': 'Standard', 'checked_in': True, 'status': 'registered'},
            {'user': u_sarah, 'event_id': 6, 'ticket': 'Standard', 'checked_in': False, 'status': 'registered'},
            {'user': u_david, 'event_id': 2, 'ticket': 'Standard', 'checked_in': True, 'status': 'registered'},
            {'user': u_david, 'event_id': 8, 'ticket': 'VIP', 'checked_in': True, 'status': 'registered'},
            {'user': u_david, 'event_id': 4, 'ticket': 'Standard', 'checked_in': False, 'status': 'registered'},
            {'user': u_priya, 'event_id': 1, 'ticket': 'Standard', 'checked_in': True, 'status': 'registered'},
            {'user': u_priya, 'event_id': 4, 'ticket': 'VIP', 'checked_in': True, 'status': 'registered'},
            {'user': u_priya, 'event_id': 7, 'ticket': 'Standard', 'checked_in': True, 'status': 'registered'},
            {'user': u_marcus, 'event_id': 3, 'ticket': 'VIP', 'checked_in': True, 'status': 'registered'},
            {'user': u_marcus, 'event_id': 5, 'ticket': 'Speaker', 'checked_in': False, 'status': 'registered'}
        ]

        for rd in regs_seed:
            if not rd['user']:
                continue
            existing_r = Registration.query.filter_by(user_id=rd['user'].id, event_id=rd['event_id']).first()
            if not existing_r:
                r = Registration(
                    user_id=rd['user'].id,
                    event_id=rd['event_id'],
                    ticket_type=rd['ticket'],
                    checked_in=rd['checked_in'],
                    status=rd['status'],
                    registered_at=now - timedelta(days=5, hours=rd['event_id'])
                )
                db.session.add(r)
            else:
                existing_r.ticket_type = rd['ticket']
                existing_r.checked_in = rd['checked_in']
                existing_r.status = rd['status']
        db.session.commit()
        print("  + Registrations synchronized.")

        # ---------------- 8. REMINDERS ----------------
        reminders_data = [
            {
                'user': u_alex,
                'event_id': 1,
                'remind_at': now + timedelta(days=2),
                'message': 'AI Summit 2026 starts at 09:00 AM at Main Grand Auditorium. Check in at Kiosk #1.',
                'sent': False
            },
            {
                'user': u_alex,
                'event_id': 2,
                'remind_at': now + timedelta(days=7),
                'message': 'Hackathon Night starts at 06:00 PM at Silicon Hall Alpha. Bring your laptop and charger!',
                'sent': False
            },
            {
                'user': u_sarah,
                'event_id': 3,
                'remind_at': now + timedelta(days=14),
                'message': 'Global FinTech Expo keynote session begins at 10:00 AM at Exhibition Pavilion.',
                'sent': False
            }
        ]
        for rem in reminders_data:
            if not rem['user']:
                continue
            existing_rem = Reminder.query.filter_by(user_id=rem['user'].id, event_id=rem['event_id']).first()
            if not existing_rem:
                rm = Reminder(
                    user_id=rem['user'].id,
                    event_id=rem['event_id'],
                    remind_at=rem['remind_at'],
                    message=rem['message'],
                    sent=rem['sent'],
                    created_at=now - timedelta(days=1)
                )
                db.session.add(rm)
        db.session.commit()
        print("  + Reminders synchronized.")

        # ---------------- 9. NOTIFICATIONS ----------------
        notifs_data = [
            {
                'recipient': 'user@eventops.com',
                'channel': 'email',
                'subject': 'Welcome to EventOps AI Platform!',
                'message': 'Hello Alex, your account is activated. Explore upcoming conferences, workshops, and AI-assisted registrations.',
                'sent_at': now - timedelta(days=4),
                'read': True
            },
            {
                'recipient': 'user@eventops.com',
                'channel': 'email',
                'subject': 'Registration Confirmed: AI Summit 2026',
                'message': 'Your VIP All-Access ticket for AI Summit 2026 has been issued. Your badge is ready for fast-track QR check-in.',
                'sent_at': now - timedelta(days=2),
                'read': True
            },
            {
                'recipient': 'user@eventops.com',
                'channel': 'sms',
                'subject': 'Event Reminder: Hackathon Night',
                'message': 'Hackathon Night check-in begins at 05:30 PM at Silicon Hall Alpha. Food and swag bags will be distributed at desk B.',
                'sent_at': now - timedelta(hours=6),
                'read': False
            },
            {
                'recipient': 'admin@eventops.com',
                'channel': 'push',
                'subject': 'Multi-Agent Ops Alert: Wi-Fi Restored',
                'message': 'Automated telemetry confirms access points 12-16 packet drops have dropped to 0.02%. Incident marked resolved.',
                'sent_at': now - timedelta(hours=1, minutes=40),
                'read': True
            },
            {
                'recipient': 'admin@eventops.com',
                'channel': 'email',
                'subject': 'Titanium Sponsor Deliverable Verified',
                'message': 'Google Cloud live keynote stage banner and digital telemetry wall have been approved by event director.',
                'sent_at': now - timedelta(hours=8),
                'read': True
            },
            {
                'recipient': 'all@eventops.com',
                'channel': 'email',
                'subject': 'EventOps Platform 2.0 Live Announcement',
                'message': 'The complete EventOps suite is now online with intelligent scheduling, live venue utilization, and interactive attendee feedback.',
                'sent_at': now - timedelta(days=1),
                'read': False
            }
        ]
        for nd in notifs_data:
            existing_n = Notification.query.filter_by(subject=nd['subject'], recipient=nd['recipient']).first()
            if not existing_n:
                n = Notification(
                    recipient=nd['recipient'],
                    channel=nd['channel'],
                    subject=nd['subject'],
                    message=nd['message'],
                    sent_at=nd['sent_at'],
                    read=nd['read']
                )
                db.session.add(n)
        db.session.commit()
        print("  + Notifications synchronized.")

        # ---------------- 10. FEEDBACK ----------------
        feedbacks_data = [
            {
                'user': u_alex,
                'event_id': 7,
                'rating': 5,
                'comment': 'Outstanding organization! The keynote on autonomous agents set a very high bar. Check-in was fast and smooth.',
                'created_at': now - timedelta(days=18)
            },
            {
                'user': u_sarah,
                'event_id': 7,
                'rating': 4,
                'comment': 'Really informative sessions and high caliber speakers. Would love 10 extra minutes between tracks for networking.',
                'created_at': now - timedelta(days=17)
            },
            {
                'user': u_david,
                'event_id': 8,
                'rating': 5,
                'comment': 'The live chaos engineering demo was extraordinary. Learned practical mitigation techniques we will use at work immediately.',
                'created_at': now - timedelta(hours=2)
            },
            {
                'user': u_priya,
                'event_id': 7,
                'rating': 5,
                'comment': 'Flawless venue facilities, crystal clear AV, and delicious catering. The digital badge scanning made entry instant!',
                'created_at': now - timedelta(days=15)
            },
            {
                'user': u_marcus,
                'event_id': 8,
                'rating': 4,
                'comment': 'Very deep technical insights into site reliability. Looking forward to the FinTech Expo next month!',
                'created_at': now - timedelta(hours=1)
            }
        ]
        for fd in feedbacks_data:
            if not fd['user']:
                continue
            existing_fb = Feedback.query.filter_by(user_id=fd['user'].id, event_id=fd['event_id']).first()
            if not existing_fb:
                fb = Feedback(
                    user_id=fd['user'].id,
                    event_id=fd['event_id'],
                    rating=fd['rating'],
                    comment=fd['comment'],
                    created_at=fd['created_at']
                )
                db.session.add(fb)
            else:
                existing_fb.rating = fd['rating']
                existing_fb.comment = fd['comment']
        db.session.commit()
        print("  + Feedbacks synchronized.")

        print("✨ Database successfully seeded with 100% complete data!")

if __name__ == '__main__':
    seed()
