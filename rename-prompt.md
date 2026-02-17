You are a naming assistant. Given a list of file paths and minimal context from a static website, suggest a new filename (basename only, same extension) for each file. Rules:
- Lowercase, kebab-case, no spaces. SEO-friendly and human-readable.
- For HTML: use page purpose (e.g. about-us.html, contact.html). Keep index.html as index.html.
- For CSS/JS: use purpose (e.g. main-styles.css, analytics.js).
- For images: use content (e.g. logo-infygate.webp, hero-banner.webp). Use alt/title when provided.
- Return a JSON object: keys = exact original path strings, values = new basename only (e.g. "main.css"). Preserve extension.
- Do not change path prefix (e.g. css/ stays css/ by returning "name.css" not "css/name.css").

Files and context:
[
  {
    "path": "404.html",
    "context": {
      "title": "",
      "first_heading": "404"
    }
  },
  {
    "path": "Academic-Coaching-Help.html",
    "context": {
      "title": "Academic Writing Help",
      "first_heading": "Academic Coaching for UK Students: Start your Success with Writing Rodgers"
    }
  },
  {
    "path": "Accounting-Assignment-Help.html",
    "context": {
      "title": "Accounting Assignment Help",
      "first_heading": "Are you struggling with Accounting Assignments?Let Writing Rodgers Guide You!"
    }
  },
  {
    "path": "Assignment-Help-in-Australia.html",
    "context": {
      "title": "Australia Assignment Help \u2013 Essays, Dissertations, Exam Prep | Writing Rodgers",
      "first_heading": "Assignment help in Australia: Avail Expert services offered by Writing Rodgers"
    }
  },
  {
    "path": "Assignment-Help-in-Birmingham.html",
    "context": {
      "title": "Assignment Help in Birmingham \u2013 Your Shortcut to Academic Success!",
      "first_heading": "Assignment Help in Birmingham \u2013 Your Shortcut to Academic Success!"
    }
  },
  {
    "path": "Assignment-Help-in-Bristol.html",
    "context": {
      "title": "UWE Bristol Assignment Help \u2013 Stress Less, Score More!",
      "first_heading": "Bristol\u2019s Go-To Assignment Help \u2013 Stress Less, Score More!"
    }
  },
  {
    "path": "Assignment-Help-in-Canada.html",
    "context": {
      "title": "Canada Assignment Help \u2013 Essays, Dissertations, Exam Prep | Writing Rodgers",
      "first_heading": "Studying in Canada? Get expert assignment help tailored to Canadian universities."
    }
  },
  {
    "path": "Assignment-Help-in-Cardiff.html",
    "context": {
      "title": "Top Assignment Help in Cardiff \u2013 Smart Students Choose Us!",
      "first_heading": "Top Assignment Help in Cardiff \u2013 Smart Students Choose Us!"
    }
  },
  {
    "path": "Assignment-Help-in-Glasgow.html",
    "context": {
      "title": "Get Ahead with Glasgow\u2019s Most Trusted Assignment Help!",
      "first_heading": "Get Ahead with Glasgow\u2019s Most Trusted Assignment Help!"
    }
  },
  {
    "path": "Assignment-Help-in-Leicester.html",
    "context": {
      "title": "Trusted UK Assignment Help for University Students",
      "first_heading": "Top-Rated Assignment Help in Leicester \u2013 Your Academic Lifesaver!"
    }
  },
  {
    "path": "Assignment-Help-in-Liverpool.html",
    "context": {
      "title": "Ace Your Grades with Expert Assignment Help in Liverpool!",
      "first_heading": "Ace Your Grades with Expert Assignment Help in Liverpool!"
    }
  },
  {
    "path": "Assignment-Help-in-London.html",
    "context": {
      "title": "London\u2019s Premier Assignment Help \u2013 Where Smart Students Get Smarter!",
      "first_heading": "London\u2019s Premier Assignment Help \u2013 Where Smart Students Get Smarter!"
    }
  },
  {
    "path": "Assignment-Help-in-Manchester.html",
    "context": {
      "title": "Assignment Help in Manchester \u2013 Boost Your Grades, Stress-Free!",
      "first_heading": "Assignment Help in Manchester \u2013 Boost Your Grades, Stress-Free!"
    }
  },
  {
    "path": "Assignment-Help-in-Oman-Muscat.html",
    "context": {
      "title": "Oman Assignment Help \u2013 Essays, Dissertations, Exam Prep | Writing Rodgers",
      "first_heading": "Assignment Help in Oman Muscat: Expert services for Healthcare, Marketing, and Nursing Project Management & More by Writing Rodgers"
    }
  },
  {
    "path": "Assignment-Help-in-UAE-by-Professionals.html",
    "context": {
      "title": "UAE Assignment Help \u2013 Essays, Dissertations, Exam Prep | Writing Rodgers",
      "first_heading": "Assignment help in UAE by Professionals: Get Expert support by Writing Rodgers"
    }
  },
  {
    "path": "Assignment-Help-in-UK-at-Reasonable-Price.html",
    "context": {
      "title": "Trusted UK Assignment Help at Resonable Rate!",
      "first_heading": "Studying in UK? Get expert assignment help tailored to UKuniversities"
    }
  },
  {
    "path": "Aston-University-Assignment-Help.html",
    "context": {
      "title": "Aston University Assignment Help",
      "first_heading": "Aston University Assignment Help"
    }
  },
  {
    "path": "BPP-Assignment-Help.html",
    "context": {
      "title": "BPP Assignment Help UK | Top Writers for BPP Coursework",
      "first_heading": "BPP University Assignment Help"
    }
  },
  {
    "path": "Case-Study-Assignment-help.html",
    "context": {
      "title": "Case Study Assignment Help by UK experts",
      "first_heading": "Writing Rodgers services to assist you with your case study analysis assignments"
    }
  },
  {
    "path": "Coventry-University-Assignment-Help.html",
    "context": {
      "title": "Coventry University Assignment Help \u2013 Tailored Essays & Dissertations",
      "first_heading": "Coventry University Assignment Help"
    }
  },
  {
    "path": "De-Montfort-University-Assignment-Help.html",
    "context": {
      "title": "A Grade De-Montfort University Assignment Help",
      "first_heading": "De Montfort University Assignment Help"
    }
  },
  {
    "path": "Dissertation-Writing-Help.html",
    "context": {
      "title": "MBA Dissertation Help",
      "first_heading": "Struggling with MBA Dissertation?Writing Rodgers Has Your Back!"
    }
  },
  {
    "path": "Edinburgh-University-Assignment-Help.html",
    "context": {
      "title": "Edinburgh University Assignment Help",
      "first_heading": "Edinburgh University Assignment Help"
    }
  },
  {
    "path": "Essay-Writing-Help.html",
    "context": {
      "title": "Urgent Assignment Help-Essay Writing Help",
      "first_heading": "Need Urgent Academic Essay Writing Help?"
    }
  },
  {
    "path": "Essex-University-Assignment-Help.html",
    "context": {
      "title": "Essex University Assignment Help",
      "first_heading": "Essex University Assignment Help"
    }
  },
  {
    "path": "Exam-Preparation-Help.html",
    "context": {
      "title": "Exam Preparation and Solution Help on Urgent basis",
      "first_heading": "\u201cSmart Exam Prep Starts Here \u2013 Writing Rodgers Has Your Back!\u201d"
    }
  },
  {
    "path": "IT-Assignment-Help.html",
    "context": {
      "title": "Get IT Assignments with Writing Rodgers",
      "first_heading": "Ace Your IT Assignments with Writing Rodgers"
    }
  },
  {
    "path": "Ireland-Assignment-Help.html",
    "context": {
      "title": "Get Assignment Help in Ireland \u2013 100% Plagiarism-Free",
      "first_heading": "Studying in Ireland? Get expert assignment help tailored to Irishuniversities."
    }
  },
  {
    "path": "Law-Assignment-Help.html",
    "context": {
      "title": "Law Assignmemt Help from Trusted Partners-no Shortcut",
      "first_heading": "\u201cStruggling with your Law Assignments? Let Writing Rodgers Simplify Law Assignments for You!\u201d"
    }
  },
  {
    "path": "Management-Assignment-Help.html",
    "context": {
      "title": "Management Assignment Help",
      "first_heading": "Need Management Assignment Help! DM Your Tutor Subham!"
    }
  },
  {
    "path": "Marketing-Assignment-Help.html",
    "context": {
      "title": "Marketing Assignment Help",
      "first_heading": "Struggling with Marketing Assignments?Let Writing Rodgers help you."
    }
  },
  {
    "path": "Middlesex-University-Assignment-Help.html",
    "context": {
      "title": "Middlesex University Assignment Help",
      "first_heading": "Middlesex University Assignment Help"
    }
  },
  {
    "path": "Nursing-Assignment-Help.html",
    "context": {
      "title": "Nursing Assignment Help in UK and Australia",
      "first_heading": "Nursing assignment help"
    }
  },
  {
    "path": "Project-Management-Assignment-Help.html",
    "context": {
      "title": "Writing Rodgers | Value Your Education| UK University Assignment Help",
      "first_heading": "\u201cPlan, Execute, succeed \u2013 Get Expert Project Management Assignment Help with Writing Rodgers\u201d"
    }
  },
  {
    "path": "Report-Writing-Help.html",
    "context": {
      "title": "Report Writing Help from MBA grduates in UK",
      "first_heading": "\u201cNeed Help with Report Writing? Let Writing Rodgers Help You Out!\u201d"
    }
  },
  {
    "path": "Thesis-Writing-Help.html",
    "context": {
      "title": "Thesis Writing Help UK | SPSS Editorial Support | Writing Rodgers",
      "first_heading": "Professional Thesis Writing Help in the UK?"
    }
  },
  {
    "path": "Thesis-with-SPSS-Nvivo-Help.html",
    "context": {
      "title": "SPSS anad NVivo Analysis in Thesis by Best level Experts!",
      "first_heading": "Crack Your Thesis with Expert Help from Writing Rodgers in SPSS & NVivo Analysis"
    }
  },
  {
    "path": "University-College-Birmingham-Assignment-Help.html",
    "context": {
      "title": "University College Birmingham Assignment Help",
      "first_heading": "University College Birmingham Assignment Help"
    }
  },
  {
    "path": "University-of-Derby-Assignment-Help.html",
    "context": {
      "title": "University of Derby Assignment Help",
      "first_heading": "University of Derby Assignment Help"
    }
  },
  {
    "path": "University-of-East-London-Assignment-Help.html",
    "context": {
      "title": "University of East London Assignment Help",
      "first_heading": "University of East London Assignment Help"
    }
  },
  {
    "path": "University-of-Greenwich-Assignment-Help.html",
    "context": {
      "title": "University of Greenwich Assignment Help",
      "first_heading": "University of Greenwich Assignment Help"
    }
  },
  {
    "path": "University-of-Salford-Assignment-Help.html",
    "context": {
      "title": "University of Salford Assignment Help",
      "first_heading": "University of Salford Assignment Help"
    }
  },
  {
    "path": "University-of-Sunderland-Assignment-Help.html",
    "context": {
      "title": "University of Sunderland Assignment Help",
      "first_heading": "University of Sunderland Assignment Help"
    }
  },
  {
    "path": "University-of-Warwick-Assignment-Help.html",
    "context": {
      "title": "University of Warwick Assignment Help",
      "first_heading": "University of Warwick Assignment Help"
    }
  },
  {
    "path": "blog.html",
    "context": {
      "title": "PSW visa tips with services",
      "first_heading": "Study in the UK and Unlock Opportunities with the PSW Visa"
    }
  },
  {
    "path": "css/3963506a1ef49308b433d9563bda0544.css",
    "context": {
      "path": "css/3963506a1ef49308b433d9563bda0544.css"
    }
  },
  {
    "path": "css/559e64bf161e61fa0aca6e864c78191d.css",
    "context": {
      "path": "css/559e64bf161e61fa0aca6e864c78191d.css"
    }
  },
  {
    "path": "css/595cb6ccb56826a802ed411cef875f0e.css",
    "context": {
      "path": "css/595cb6ccb56826a802ed411cef875f0e.css"
    }
  },
  {
    "path": "css/5ecf9a22a9fea377b8fd4e5d4a7d1a70.css",
    "context": {
      "path": "css/5ecf9a22a9fea377b8fd4e5d4a7d1a70.css"
    }
  },
  {
    "path": "css/6a26902ae7710ea31582d01a2a58d35d.css",
    "context": {
      "path": "css/6a26902ae7710ea31582d01a2a58d35d.css"
    }
  },
  {
    "path": "css/6d95c421cfdc25743ca3bee482775041.css",
    "context": {
      "path": "css/6d95c421cfdc25743ca3bee482775041.css"
    }
  },
  {
    "path": "css/84d4a0216f16f715d9b301db3a8da352.css",
    "context": {
      "path": "css/84d4a0216f16f715d9b301db3a8da352.css"
    }
  },
  {
    "path": "css/99c4e6f40ee9111eea53b6472f3e60f9.css",
    "context": {
      "path": "css/99c4e6f40ee9111eea53b6472f3e60f9.css"
    }
  },
  {
    "path": "css/d09d646f062b67daeff66ff1410b63fc.css",
    "context": {
      "path": "css/d09d646f062b67daeff66ff1410b63fc.css"
    }
  },
  {
    "path": "css/d43f42026bdbe6ae7437833b53c39e0c.css",
    "context": {
      "path": "css/d43f42026bdbe6ae7437833b53c39e0c.css"
    }
  },
  {
    "path": "css/dcd8e46ff1981f7ebf74247b65b562b4.css",
    "context": {
      "path": "css/dcd8e46ff1981f7ebf74247b65b562b4.css"
    }
  },
  {
    "path": "css/internal-styles.css",
    "context": {
      "path": "css/internal-styles.css"
    }
  },
  {
    "path": "imgs/0228e0de61dff0809d09d32157ddf05a.webp",
    "context": {
      "refs": [
        {
          "alt": "Essex Assignment Help, Essex University Assignment Help, Essex University study, Essex University Co",
          "title": ""
        }
      ]
    }
  },
  {
    "path": "imgs/0271194bfd745aa9d19ee69509fecd8f.webp",
    "context": {
      "refs": [
        {
          "alt": "",
          "title": ""
        }
      ]
    }
  },
  {
    "path": "imgs/0502d879cde504e98035b537709b5662.webp",
    "context": {
      "refs": [
        {
          "alt": "Presentation",
          "title": ""
        }
      ]
    }
  },
  {
    "path": "imgs/0a5dc3cc6f3761f371058a61085f16af.webp",
    "context": {
      "refs": [
        {
          "alt": "#assignmenthelpuk #ukuniversities #indiatouk, #writingrodgers,",
          "title": ""
        }
      ]
    }
  },
  {
    "path": "imgs/0d367a19bbfdcf628fd5e0b001213aed.webp",
    "context": {
      "refs": [
        {
          "alt": "Middlesex Assignment Help, Middlesex University Assignment Help, Middlesex University study, Middles",
          "title": ""
        },
        {
          "alt": "University of East London Assignment Help, UEL Assignment Help, University of East London study, Uni",
          "title": ""
        },
        {
          "alt": "Edinburgh University Assignment Help, Edinburgh Assignment Help, Ediburgh University study, Edinburg",
          "title": ""
        },
        {
          "alt": "University of Warwick Assignment Help, University of Warwick Assignment Help, University of Warwick ",
          "title": ""
        },
        {
          "alt": "University of Salford, University of Salford Assignment Help, Salford University study, Salford Univ",
          "title": ""
        },
        {
          "alt": "University of Greenwich Assignment Help, University of Greenwich Assignment Help, University of Gree",
          "title": ""
        },
        {
          "alt": "University of Derby Assignment Help, University of Derby Assignment Help, University of Derby study,",
          "title": ""
        },
        {
          "alt": "University of Sunderland Assignment Help, University of Sunderland Assignment Help, University of Su",
          "title": ""
        },
        {
          "alt": "Essex Assignment Help, Essex University Assignment Help, Essex University study, Essex University Co",
          "title": ""
        },
        {
          "alt": "DMU Assignment Help, DMU University Assignment Help, DMU University study, DMU University Courses, D",
          "title": ""
        },
        {
          "alt": "BPP Assignment help in UK, BPP University study, BPP University Courses, BPP Assignment Help, BPP Un",
          "title": ""
        },
        {
          "alt": "Univrsity College Birmingham Assignment Help, UCB University Assignment Help, UCB University study, ",
          "title": ""
        }
      ]
    }
  },
  {
    "path": "imgs/11494b7742b438ba66a49393d67da326.webp",
    "context": {
      "refs": [
        {
          "alt": "Assignment Help in UAE, UAE Exam Help, Cookery Assignment Help, Accounting Assignment Help in UAE, N",
          "title": ""
        }
      ]
    }
  },
  {
    "path": "imgs/11dc014a902fd7b195a749ed087f39a6.webp",
    "context": {
      "refs": [
        {
          "alt": "Essay Writing Help, Urgent Assignment Help, UK University study, MbA Essay Topics, Essay, Reports, P",
          "title": ""
        }
      ]
    }
  },
  {
    "path": "imgs/123492b5666808336ad8b15e29dadc56.webp",
    "context": {
      "refs": [
        {
          "alt": "IT Assignment Help, IT management Assignment Help, dissertation and thesis help, assignment help IT,",
          "title": ""
        }
      ]
    }
  },
  {
    "path": "imgs/153a6f705cf6525fc607023ab860553e.webp",
    "context": {
      "refs": [
        {
          "alt": "Assignment help, writing rodgers solution, writing rodgers solution subham, workingment, dissertatio",
          "title": ""
        }
      ]
    }
  },
  {
    "path": "imgs/15d9caf8ed979dc1ac6201056a1d444a.webp",
    "context": {
      "refs": [
        {
          "alt": "Middlesex Assignment Help, Middlesex University Assignment Help, Middlesex University study, Middles",
          "title": ""
        },
        {
          "alt": "University of East London Assignment Help, UEL Assignment Help, University of East London study, Uni",
          "title": ""
        },
        {
          "alt": "Edinburgh University Assignment Help, Edinburgh Assignment Help, Ediburgh University study, Edinburg",
          "title": ""
        },
        {
          "alt": "University of Salford, University of Salford Assignment Help, Salford University study, Salford Univ",
          "title": ""
        },
        {
          "alt": "DMU Assignment Help, DMU University Assignment Help, DMU University study, DMU University Courses, D",
          "title": ""
        },
        {
          "alt": "BPP Assignment help in UK, BPP University study, BPP University Courses, BPP Assignment Help, BPP Un",
          "title": ""
        }
      ]
    }
  },
  {
    "path": "imgs/17dca0d039d004e922a30733f984cc78.webp",
    "context": {
      "refs": [
        {
          "alt": "",
          "title": ""
        }
      ]
    }
  },
  {
    "path": "imgs/17f25335571a91429d6ec40955822925.webp",
    "context": {
      "refs": [
        {
          "alt": "Assignment Help in Canada, Australia Exam Help, Cookery Assignment Help, Accounting Assignment Help ",
          "title": ""
        }
      ]
    }
  },
  {
    "path": "imgs/263d04953da1540ff0b633c7d75b8e6f.webp",
    "context": {
      "refs": [
        {
          "alt": "",
          "title": ""
        }
      ]
    }
  },
  {
    "path": "imgs/274b0ab5e14331c558c559da34ed45c1.webp",
    "context": {
      "refs": [
        {
          "alt": "",
          "title": ""
        }
      ]
    }
  },
  {
    "path": "imgs/2781d9a53a9ff6e832919a41ff27e27f.webp",
    "context": {
      "refs": [
        {
          "alt": "",
          "title": ""
        }
      ]
    }
  },
  {
    "path": "imgs/294ad3ea2a781fdfbf46aca8efd57fc7.webp",
    "context": {
      "refs": [
        {
          "alt": "",
          "title": ""
        }
      ]
    }
  },
  {
    "path": "imgs/2fd1762968a564f40d636e72614282b8.webp",
    "context": {
      "refs": [
        {
          "alt": "Marketing Assignment Help, Marketing Assignment Help, Marketing Study in UK, UK University Marketing",
          "title": ""
        }
      ]
    }
  },
  {
    "path": "imgs/30b4f21c1b9191165543169cf87cc338.webp",
    "context": {
      "refs": [
        {
          "alt": "University of Sunderland Assignment Help, University of Sunderland Assignment Help, University of Su",
          "title": ""
        }
      ]
    }
  },
  {
    "path": "imgs/3b4e8e98e9b29c4683968da28ded6ad2.webp",
    "context": {
      "refs": [
        {
          "alt": "University of Derby Assignment Help, University of Derby Assignment Help, University of Derby study,",
          "title": ""
        }
      ]
    }
  },
  {
    "path": "imgs/3f332618cd277f5cc44f7312283c51fe.webp",
    "context": {
      "refs": [
        {
          "alt": "Management Assignment Help, MBA Assignment Help, Managemnt Study in UK University , UK MBA Courses, ",
          "title": ""
        }
      ]
    }
  },
  {
    "path": "imgs/4226bf03b6933698fba145cc5cb4e821.webp",
    "context": {
      "refs": [
        {
          "alt": "MBA Dissertation Help, MBA Thesis Help, MBA Dissertation Topics, UK Dissertation Ethics, Essay, Repo",
          "title": ""
        }
      ]
    }
  },
  {
    "path": "imgs/46ac5f501256691af70d73a182851d0d.webp",
    "context": {
      "refs": [
        {
          "alt": "Online tutoring",
          "title": ""
        }
      ]
    }
  },
  {
    "path": "imgs/4f7b51e8c899d436016bb64bc38aef99.webp",
    "context": {
      "refs": [
        {
          "alt": "Law Assignment Help, Thesis Help on Law, Law Dissertation Help, Law Report Writing, Law Essay Help, ",
          "title": ""
        }
      ]
    }
  },
  {
    "path": "imgs/50a3e02d061d3232a60c24bb233cc7f1.webp",
    "context": {
      "refs": [
        {
          "alt": "Case Study Assignment Help, dissertation and thesis help, assignment help, help with assignments, he",
          "title": ""
        }
      ]
    }
  },
  {
    "path": "imgs/54eeca5d5d1143e13f994dfe134c8d20.webp",
    "context": {
      "refs": [
        {
          "alt": "Essex Assignment Help, Essex University Assignment Help, Essex University study, Essex University Co",
          "title": ""
        }
      ]
    }
  },
  {
    "path": "imgs/5dd0d6cc6773bec876be10a3cc4e62ce.webp",
    "context": {
      "refs": [
        {
          "alt": "Thesis Writing Help, Thesis with SPSS analysis Help, SPSS Assignment Help, Quantitative Research Exa",
          "title": ""
        }
      ]
    }
  },
  {
    "path": "imgs/60463068d686d482087238a5c6f2ab1c.webp",
    "context": {
      "refs": [
        {
          "alt": "",
          "title": ""
        }
      ]
    }
  },
  {
    "path": "imgs/61b8afd7c2428b691a9a44306a45a069.webp",
    "context": {
      "refs": [
        {
          "alt": "University of Greenwich Assignment Help, University of Greenwich Assignment Help, University of Gree",
          "title": ""
        }
      ]
    }
  },
  {
    "path": "imgs/65a11affc2749cde6b47ff2c820076ab.webp",
    "context": {
      "refs": [
        {
          "alt": "BPP Assignment Help, BPP University Assignment Help, BPP University study, BPP University Courses, E",
          "title": ""
        }
      ]
    }
  },
  {
    "path": "imgs/65c65991c6ee2237a08280e4e7b4ce4d.webp",
    "context": {
      "refs": [
        {
          "alt": "",
          "title": ""
        }
      ]
    }
  },
  {
    "path": "imgs/6a19d70a9d83a7346e28406ef7446ca6.webp",
    "context": {
      "refs": [
        {
          "alt": "",
          "title": ""
        }
      ]
    }
  },
  {
    "path": "imgs/6a59a3edc39ba3a37bdda27941484e4e.webp",
    "context": {
      "refs": [
        {
          "alt": "Reports",
          "title": ""
        }
      ]
    }
  },
  {
    "path": "imgs/6aae13a34d86e8820a129bc366fa48cd.webp",
    "context": {
      "refs": [
        {
          "alt": "",
          "title": ""
        }
      ]
    }
  },
  {
    "path": "imgs/6aea126c6a3e2e67382b58809d24c655.webp",
    "context": {
      "refs": [
        {
          "alt": "Assignment Help in Ireland, Ireland Exam Help, Dissertation Writing Help in Ireland, Accounting Assi",
          "title": ""
        }
      ]
    }
  },
  {
    "path": "imgs/6fd575fd4331be36337256702194b9de.webp",
    "context": {
      "refs": [
        {
          "alt": "BPP Assignment Help, BPP University Assignment Help, BPP University study, BPP University Courses, E",
          "title": ""
        }
      ]
    }
  },
  {
    "path": "imgs/810339c25560ff4b2daaa13b89d1d05d.webp",
    "context": {
      "refs": [
        {
          "alt": "Aston Assignment Help, Aston University Assignment Help, Aston University study, Aston University Co",
          "title": ""
        }
      ]
    }
  },
  {
    "path": "imgs/8368cccf8612ba5aef7205ba6fb3e0a4.webp",
    "context": {
      "refs": [
        {
          "alt": "Middlesex Assignment Help, Middlesex University Assignment Help, Middlesex University study, Middles",
          "title": ""
        },
        {
          "alt": "University of East London Assignment Help, UEL Assignment Help, University of East London study, Uni",
          "title": ""
        },
        {
          "alt": "Edinburgh University Assignment Help, Edinburgh Assignment Help, Ediburgh University study, Edinburg",
          "title": ""
        },
        {
          "alt": "University of Warwick Assignment Help, University of Warwick Assignment Help, University of Warwick ",
          "title": ""
        },
        {
          "alt": "University of Salford, University of Salford Assignment Help, Salford University study, Salford Univ",
          "title": ""
        },
        {
          "alt": "Aston Assignment Help, Aston University Assignment Help, Aston University study, Aston University Co",
          "title": ""
        },
        {
          "alt": "University of Greenwich Assignment Help, University of Greenwich Assignment Help, University of Gree",
          "title": ""
        },
        {
          "alt": "University of Derby Assignment Help, University of Derby Assignment Help, University of Derby study,",
          "title": ""
        },
        {
          "alt": "Coventry University Assignment Help, Coventry Assignment Help, Coventry University study, Coventry U",
          "title": ""
        },
        {
          "alt": "University of Sunderland Assignment Help, University of Sunderland Assignment Help, University of Su",
          "title": ""
        },
        {
          "alt": "Essex Assignment Help, Essex University Assignment Help, Essex University study, Essex University Co",
          "title": ""
        },
        {
          "alt": "Assignment Help in UK, UK Exam Help, Dissertation Writing Help in UK, Accounting Assignment Help in ",
          "title": ""
        },
        {
          "alt": "DMU Assignment Help, DMU University Assignment Help, DMU University study, DMU University Courses, D",
          "title": ""
        },
        {
          "alt": "BPP Assignment Help, BPP University Assignment Help, BPP University study, BPP University Courses, E",
          "title": ""
        },
        {
          "alt": "Assignment Help in UK, UK assignment help, Assignment help UK, Online assignment help UK, Best assig",
          "title": ""
        },
        {
          "alt": "Univrsity College Birmingham Assignment Help, UCB University Assignment Help, UCB University study, ",
          "title": ""
        }
      ]
    }
  },
  {
    "path": "imgs/83b659b5e1dcfbf548f53a6a4fee0e34.webp",
    "context": {
      "refs": [
        {
          "alt": "Assignment Help in Oman, Oman Exam Help, Cookery Assignment Help, Accounting Assignment Help in Oman",
          "title": ""
        }
      ]
    }
  },
  {
    "path": "imgs/83f5c43ba3ecde831623607a97cbeecf.webp",
    "context": {
      "refs": [
        {
          "alt": "Dissertation",
          "title": ""
        }
      ]
    }
  },
  {
    "path": "imgs/888f3a36d0ae4ddf927f94870d82ca35.webp",
    "context": {
      "refs": [
        {
          "alt": "",
          "title": ""
        }
      ]
    }
  },
  {
    "path": "imgs/90526a1ea6cf6618aac313ed0859da65.webp",
    "context": {
      "refs": [
        {
          "alt": "Academic Writing Help, MBA Assignment Help, Academic Coaching Support, Academic Writing Courses, Ess",
          "title": ""
        }
      ]
    }
  },
  {
    "path": "imgs/92d285ab5eeca4675401bb3460eae6ce.webp",
    "context": {
      "refs": [
        {
          "alt": "University of Derby Assignment Help, University of Derby Assignment Help, University of Derby study,",
          "title": ""
        }
      ]
    }
  },
  {
    "path": "imgs/95e2504ac6a9056eb4c79ed4f3764362.webp",
    "context": {
      "refs": [
        {
          "alt": "Thesis Writing Help, Nursing Thesis Writing Help, MBA Thesis Topics,UK University Dissertation Topic",
          "title": ""
        }
      ]
    }
  },
  {
    "path": "imgs/9cfb392895788a484eb47b0791d080ad.webp",
    "context": {
      "refs": [
        {
          "alt": "Assignment help Glasgow, University of Glasgow assignment help, Glasgow Caledonian assignment writin",
          "title": ""
        },
        {
          "alt": "Assignment help Birmingham, University of Birmingham assignment help, Birmingham City University ass",
          "title": ""
        },
        {
          "alt": "Assignment Help in UK, UK Exam Help, Dissertation Writing Help in UK, Accounting Assignment Help in ",
          "title": ""
        },
        {
          "alt": "Assignment help Cardiff, Cardiff University assignment help, Essay writing service Cardiff, Disserta",
          "title": ""
        },
        {
          "alt": "Affordable assignment help for University of Manchester students, Urgent assignment writing service ",
          "title": ""
        },
        {
          "alt": "Assignment help Bristol, University of Bristol assignment help, UWE Bristol academic writing service",
          "title": ""
        }
      ]
    }
  },
  {
    "path": "imgs/a608ccdd93823697e3a8ab546f2792c5.webp",
    "context": {
      "refs": [
        {
          "alt": "Diploma works",
          "title": ""
        }
      ]
    }
  },
  {
    "path": "imgs/a61c89e57112cfe98c4d1812bfa18c20.webp",
    "context": {
      "refs": [
        {
          "alt": "BPP Assignment Help, BPP University Assignment Help, BPP University study, BPP University Courses, E",
          "title": ""
        }
      ]
    }
  },
  {
    "path": "imgs/a6f8639a635195f8f2fb50442cd58e1a.webp",
    "context": {
      "refs": [
        {
          "alt": "logo",
          "title": ""
        },
        {
          "alt": "logo",
          "title": ""
        },
        {
          "alt": "logo",
          "title": ""
        },
        {
          "alt": "logo",
          "title": ""
        },
        {
          "alt": "logo",
          "title": ""
        },
        {
          "alt": "logo",
          "title": ""
        },
        {
          "alt": "logo",
          "title": ""
        },
        {
          "alt": "logo",
          "title": ""
        },
        {
          "alt": "logo",
          "title": ""
        },
        {
          "alt": "logo",
          "title": ""
        },
        {
          "alt": "logo",
          "title": ""
        },
        {
          "alt": "logo",
          "title": ""
        },
        {
          "alt": "logo",
          "title": ""
        },
        {
          "alt": "logo",
          "title": ""
        },
        {
          "alt": "logo",
          "title": ""
        },
        {
          "alt": "logo",
          "title": ""
        },
        {
          "alt": "logo",
          "title": ""
        },
        {
          "alt": "logo",
          "title": ""
        },
        {
          "alt": "logo",
          "title": ""
        },
        {
          "alt": "logo",
          "title": ""
        },
        {
          "alt": "logo",
          "title": ""
        },
        {
          "alt": "logo",
          "title": ""
        },
        {
          "alt": "logo",
          "title": ""
        },
        {
          "alt": "logo",
          "title": ""
        },
        {
          "alt": "logo",
          "title": ""
        },
        {
          "alt": "logo",
          "title": ""
        },
        {
          "alt": "logo",
          "title": ""
        },
        {
          "alt": "logo",
          "title": ""
        },
        {
          "alt": "logo",
          "title": ""
        },
        {
          "alt": "logo",
          "title": ""
        },
        {
          "alt": "logo",
          "title": ""
        },
        {
          "alt": "logo",
          "title": ""
        },
        {
          "alt": "logo",
          "title": ""
        },
        {
          "alt": "logo",
          "title": ""
        },
        {
          "alt": "logo",
          "title": ""
        },
        {
          "alt": "logo",
          "title": ""
        },
        {
          "alt": "logo",
          "title": ""
        },
        {
          "alt": "logo",
          "title": ""
        },
        {
          "alt": "logo",
          "title": ""
        },
        {
          "alt": "logo",
          "title": ""
        },
        {
          "alt": "logo",
          "title": ""
        },
        {
          "alt": "logo",
          "title": ""
        },
        {
          "alt": "logo",
          "title": ""
        },
        {
          "alt": "logo",
          "title": ""
        },
        {
          "alt": "logo",
          "title": ""
        }
      ]
    }
  },
  {
    "path": "imgs/aaa0037c9ae7008477cc9746ce8880b0.webp",
    "context": {
      "refs": [
        {
          "alt": "Coventry University Assignment Help, Coventry Assignment Help, Coventry University study, Coventry U",
          "title": ""
        }
      ]
    }
  },
  {
    "path": "imgs/ab0f1d16f729f890b5f6205db6f0248c.webp",
    "context": {
      "refs": [
        {
          "alt": "Coventry University Assignment Help, Coventry Assignment Help, Coventry University study, Coventry U",
          "title": ""
        }
      ]
    }
  },
  {
    "path": "imgs/aed59455b8c5c53c0328ea6a6d8e0c60.webp",
    "context": {
      "refs": [
        {
          "alt": "Assignment Help in Australia, Australia Exam Help, Cookery Assignment Help, Accounting Assignment He",
          "title": ""
        }
      ]
    }
  },
  {
    "path": "imgs/b0d8a52af9705875479716cc31092feb.webp",
    "context": {
      "refs": [
        {
          "alt": "",
          "title": ""
        }
      ]
    }
  },
  {
    "path": "imgs/b4afc99626eb1eea778e1b5d2ac921d1.webp",
    "context": {
      "refs": [
        {
          "alt": "",
          "title": ""
        }
      ]
    }
  },
  {
    "path": "imgs/ba3fdda053e270155b263eb3fab77891.webp",
    "context": {
      "refs": [
        {
          "alt": "",
          "title": ""
        }
      ]
    }
  },
  {
    "path": "imgs/bc23efd9cce23b5d02ab32c19f1eb578.webp",
    "context": {
      "refs": [
        {
          "alt": "University of Warwick Assignment Help, University of Warwick Assignment Help, University of Warwick ",
          "title": ""
        },
        {
          "alt": "Aston Assignment Help, Aston University Assignment Help, Aston University study, Aston University Co",
          "title": ""
        }
      ]
    }
  },
  {
    "path": "imgs/c1815948ae21f3d7c656d0e81e7e0423.webp",
    "context": {
      "refs": [
        {
          "alt": "",
          "title": ""
        }
      ]
    }
  },
  {
    "path": "imgs/c294bd9c55266aef937daaf7869aba2b.webp",
    "context": {
      "refs": [
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        }
      ]
    }
  },
  {
    "path": "imgs/c3da8f7f68deb2f862b8e3754698647d.webp",
    "context": {
      "refs": [
        {
          "alt": "Accounting Assignment Help, Finance Assignment Help, Accounting Study in UK, Finance UK Courses, Ess",
          "title": ""
        }
      ]
    }
  },
  {
    "path": "imgs/c484eacfec8f81e0eb00b72726dcaef4.webp",
    "context": {
      "refs": [
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        }
      ]
    }
  },
  {
    "path": "imgs/c5d64888762874449b69528e8dc16033.webp",
    "context": {
      "refs": [
        {
          "alt": "Coventry University Assignment Help, Coventry Assignment Help, Coventry University study, Coventry U",
          "title": ""
        },
        {
          "alt": "Univrsity College Birmingham Assignment Help, UCB University Assignment Help, UCB University study, ",
          "title": ""
        }
      ]
    }
  },
  {
    "path": "imgs/c6450b45c110b51432467c3c50b05b96.webp",
    "context": {
      "refs": [
        {
          "alt": "Project Management Assignment Help, Thesis Help on Project Management, Supply Chain Management, Diss",
          "title": ""
        }
      ]
    }
  },
  {
    "path": "imgs/c79fca1eced7d516f20b12d40e0a3762.webp",
    "context": {
      "refs": [
        {
          "alt": "Assignment help, writing rodgers solution, writing rodgers solution subham, workingment, dissertatio",
          "title": ""
        }
      ]
    }
  },
  {
    "path": "imgs/c951b0673c3f3ac63fd8bb5b7c841817.webp",
    "context": {
      "refs": [
        {
          "alt": "",
          "title": ""
        }
      ]
    }
  },
  {
    "path": "imgs/cc99382ae2c9d7ec2534acb7dd23dba2.webp",
    "context": {
      "refs": [
        {
          "alt": "",
          "title": ""
        }
      ]
    }
  },
  {
    "path": "imgs/cd612d1034e01b86220fe1278a885577.webp",
    "context": {
      "refs": [
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        }
      ]
    }
  },
  {
    "path": "imgs/ce799733cdc8f7610b2bd02584123de2.webp",
    "context": {
      "refs": [
        {
          "alt": "BPP Assignment Help, BPP University Assignment Help, BPP University study, BPP University Courses, E",
          "title": ""
        },
        {
          "alt": "University of Warwick Assignment Help, University of Warwick Assignment Help, University of Warwick ",
          "title": ""
        },
        {
          "alt": "Aston Assignment Help, Aston University Assignment Help, Aston University study, Aston University Co",
          "title": ""
        }
      ]
    }
  },
  {
    "path": "imgs/ceb37d40eb50c6c42a5ce0ca19ba17df.webp",
    "context": {
      "refs": [
        {
          "alt": "Middlesex Assignment Help, Middlesex University Assignment Help, Middlesex University study, Middles",
          "title": ""
        },
        {
          "alt": "University of East London Assignment Help, UEL Assignment Help, University of East London study, Uni",
          "title": ""
        },
        {
          "alt": "Edinburgh University Assignment Help, Edinburgh Assignment Help, Ediburgh University study, Edinburg",
          "title": ""
        },
        {
          "alt": "University of Salford, University of Salford Assignment Help, Salford University study, Salford Univ",
          "title": ""
        },
        {
          "alt": "University of Greenwich Assignment Help, University of Greenwich Assignment Help, University of Gree",
          "title": ""
        },
        {
          "alt": "DMU Assignment Help, DMU University Assignment Help, DMU University study, DMU University Courses, D",
          "title": ""
        },
        {
          "alt": "BPP Assignment help in UK, BPP University study, BPP University Courses, BPP Assignment Help, BPP Un",
          "title": ""
        },
        {
          "alt": "Univrsity College Birmingham Assignment Help, UCB University Assignment Help, UCB University study, ",
          "title": ""
        }
      ]
    }
  },
  {
    "path": "imgs/cef4424823c5c747155124cec19720f4.webp",
    "context": {
      "refs": []
    }
  },
  {
    "path": "imgs/cf388fde510947c05bde39c165db6d3b.webp",
    "context": {
      "refs": [
        {
          "alt": "Exam Preparation Help, Urgent Exam help, Solution for exam, dissertation and thesis help, assignment",
          "title": ""
        }
      ]
    }
  },
  {
    "path": "imgs/d1a3025b4b727b99438bbbd481afb4ce.webp",
    "context": {
      "refs": [
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        },
        {
          "alt": "",
          "title": ""
        }
      ]
    }
  },
  {
    "path": "imgs/d2b0bf3bd5e25e89a0e9acbe3b9f3dfd.webp",
    "context": {
      "refs": [
        {
          "alt": "BPP Assignment Help, BPP University Assignment Help, BPP University study, BPP University Courses, E",
          "title": ""
        }
      ]
    }
  },
  {
    "path": "imgs/d57c770e7bf46f632a4617a0dcf7d538.webp",
    "context": {
      "refs": [
        {
          "alt": "Assignment Help in UK, UK Exam Help, Dissertation Writing Help in UK, Accounting Assignment Help in ",
          "title": ""
        }
      ]
    }
  },
  {
    "path": "imgs/dabf13af6c56fc7cb69bca97861e74ee.webp",
    "context": {
      "refs": [
        {
          "alt": "",
          "title": ""
        }
      ]
    }
  },
  {
    "path": "imgs/dce4d3a7f6e46f6bed8217b3f7b261b1.webp",
    "context": {
      "refs": [
        {
          "alt": "",
          "title": ""
        }
      ]
    }
  },
  {
    "path": "imgs/deb1ae8a20dd1fd277efef4e986dd145.webp",
    "context": {
      "refs": [
        {
          "alt": "Report Writing Help, Report Management Help, Report on Marketing Help, Marketing Report Help, IT man",
          "title": ""
        }
      ]
    }
  },
  {
    "path": "imgs/e81c18e1317e2c880cf3de5e11a352fe.webp",
    "context": {
      "refs": [
        {
          "alt": "",
          "title": ""
        }
      ]
    }
  },
  {
    "path": "imgs/ec1ddb7a959602a00ddd08154738b8fe.webp",
    "context": {
      "refs": [
        {
          "alt": "",
          "title": ""
        }
      ]
    }
  },
  {
    "path": "imgs/f1b5638ba0d38fe6c57ca4ffcdff3d09.webp",
    "context": {
      "refs": [
        {
          "alt": "University of Sunderland Assignment Help, University of Sunderland Assignment Help, University of Su",
          "title": ""
        }
      ]
    }
  },
  {
    "path": "imgs/f1fbcbf68d3eceee53515be2f7de735e.webp",
    "context": {
      "refs": [
        {
          "alt": "Nursing Assignment Help, Nursing Study in UK, Psychology Assignment Help, Medical Assignment Help, C",
          "title": ""
        }
      ]
    }
  },
  {
    "path": "imgs/fcb19d44efb3f909b57210b612153457.webp",
    "context": {
      "refs": [
        {
          "alt": "",
          "title": ""
        }
      ]
    }
  },
  {
    "path": "imgs/ff595444c797bd263a4c07923cc40436.webp",
    "context": {
      "refs": [
        {
          "alt": "Assignment help, writing rodgers solution, writing rodgers solution subham, workingment, dissertatio",
          "title": ""
        }
      ]
    }
  },
  {
    "path": "index.html",
    "context": {
      "title": "UK Assignment Help at Reasonable Price| Stress Less, Score More with Writing Rodgers!",
      "first_heading": "Get assignment help in UK from Expert Writers at Affordable Price!"
    }
  },
  {
    "path": "js/03b2eaae6007054a68c38e495f894dba.js",
    "context": {
      "path": "js/03b2eaae6007054a68c38e495f894dba.js"
    }
  },
  {
    "path": "js/0a105d712b6a6c836c48dd97d0f0cac1.js",
    "context": {
      "path": "js/0a105d712b6a6c836c48dd97d0f0cac1.js"
    }
  },
  {
    "path": "js/0c46896987137b0016246f6bc2243099.js",
    "context": {
      "path": "js/0c46896987137b0016246f6bc2243099.js"
    }
  },
  {
    "path": "js/165d7b0ddfa33362140feea997351b77.js",
    "context": {
      "path": "js/165d7b0ddfa33362140feea997351b77.js"
    }
  },
  {
    "path": "js/16df9ef05001a1741857bf99f5a5738f.js",
    "context": {
      "path": "js/16df9ef05001a1741857bf99f5a5738f.js"
    }
  },
  {
    "path": "js/2a85c11e395a8380b5915443e926b569.js",
    "context": {
      "path": "js/2a85c11e395a8380b5915443e926b569.js"
    }
  },
  {
    "path": "js/34be5330971fdbd18985525bd994b0aa.js",
    "context": {
      "path": "js/34be5330971fdbd18985525bd994b0aa.js"
    }
  },
  {
    "path": "js/35c5f9e096d4da33d2a62031daf14248.js",
    "context": {
      "path": "js/35c5f9e096d4da33d2a62031daf14248.js"
    }
  },
  {
    "path": "js/3d70953a848219e749fedc2cdb906675.js",
    "context": {
      "path": "js/3d70953a848219e749fedc2cdb906675.js"
    }
  },
  {
    "path": "js/3e940a33e44b65c1c0af8bb80a893530.js",
    "context": {
      "path": "js/3e940a33e44b65c1c0af8bb80a893530.js"
    }
  },
  {
    "path": "js/544d012df7acf9c3f0920f67c9e322b9.js",
    "context": {
      "path": "js/544d012df7acf9c3f0920f67c9e322b9.js"
    }
  },
  {
    "path": "js/57d119d998d518b01f9d5ccb5e4d4c52.js",
    "context": {
      "path": "js/57d119d998d518b01f9d5ccb5e4d4c52.js"
    }
  },
  {
    "path": "js/67f6e2f99c3c3133e0dc669919fff5c5.js",
    "context": {
      "path": "js/67f6e2f99c3c3133e0dc669919fff5c5.js"
    }
  },
  {
    "path": "js/7045b35c5bd0e9c7cf59f1900eeeec41.js",
    "context": {
      "path": "js/7045b35c5bd0e9c7cf59f1900eeeec41.js"
    }
  },
  {
    "path": "js/7260bab328b0ad74815a5efb377bcc67.js",
    "context": {
      "path": "js/7260bab328b0ad74815a5efb377bcc67.js"
    }
  },
  {
    "path": "js/893de96f1b6da546bd7c814964723eca.js",
    "context": {
      "path": "js/893de96f1b6da546bd7c814964723eca.js"
    }
  },
  {
    "path": "js/93e29fe348ddc9b71aba9c842adc18b8.js",
    "context": {
      "path": "js/93e29fe348ddc9b71aba9c842adc18b8.js"
    }
  },
  {
    "path": "js/9455859483e31e4da0e28f10d0742c2a.js",
    "context": {
      "path": "js/9455859483e31e4da0e28f10d0742c2a.js"
    }
  },
  {
    "path": "js/9db10375d298678e53777a2347b87073.js",
    "context": {
      "path": "js/9db10375d298678e53777a2347b87073.js"
    }
  },
  {
    "path": "js/9f9b6e54f82a6bbc8bac9b89327024bc.js",
    "context": {
      "path": "js/9f9b6e54f82a6bbc8bac9b89327024bc.js"
    }
  },
  {
    "path": "js/9fbfb77173c1c89b989441193826b267.js",
    "context": {
      "path": "js/9fbfb77173c1c89b989441193826b267.js"
    }
  },
  {
    "path": "js/a2261649751fa61b606222c9b2ea3b80.js",
    "context": {
      "path": "js/a2261649751fa61b606222c9b2ea3b80.js"
    }
  },
  {
    "path": "js/b0bade6d42c2702ca85774296cc507c4.js",
    "context": {
      "path": "js/b0bade6d42c2702ca85774296cc507c4.js"
    }
  },
  {
    "path": "js/cd1ed86c1e7f06d985fd71bc10bd4b04.js",
    "context": {
      "path": "js/cd1ed86c1e7f06d985fd71bc10bd4b04.js"
    }
  },
  {
    "path": "js/cecb447a04bbe3e8982190dd6e697120.js",
    "context": {
      "path": "js/cecb447a04bbe3e8982190dd6e697120.js"
    }
  },
  {
    "path": "js/d80b370d82680fc786dcc943a327b9f2.js",
    "context": {
      "path": "js/d80b370d82680fc786dcc943a327b9f2.js"
    }
  },
  {
    "path": "js/df80c5cbcb312a9c7c0b2ebb6ac5f592.js",
    "context": {
      "path": "js/df80c5cbcb312a9c7c0b2ebb6ac5f592.js"
    }
  },
  {
    "path": "js/f1e5dbc1ece900d164c2e9aa2d6a1386.js",
    "context": {
      "path": "js/f1e5dbc1ece900d164c2e9aa2d6a1386.js"
    }
  },
  {
    "path": "js/f3f02c438592c8e1bbe551f4dbbf4f5c.js",
    "context": {
      "path": "js/f3f02c438592c8e1bbe551f4dbbf4f5c.js"
    }
  }
]

Return only a JSON object mapping each path to its new basename (same extension). No other text.