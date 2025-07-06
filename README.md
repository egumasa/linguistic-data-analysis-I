# Linguistic Data Analysis I

**Course Title**: Linguistic Data Analysis I  
**Instructor**: [Your Name]  
**Institution**: Tohoku University  
**Term**: [Spring/Fall] 2025  

## Course Description

This graduate-level course introduces students to corpus linguistics and learner language analysis. Students will learn to use computational tools to analyze linguistic data, with a focus on learner corpora and practical applications.

## Navigation

| Section | Description |
|---------|-------------|
| [Syllabus](syllabus/) | Course information, schedule, and policies |
| [Sessions](sessions/) | Daily materials, slides, and activities |
| [Assignments](assignments/) | Hands-on assignments and final project |
| [Resources](resources/) | Tools, corpora, and code examples |
| [Student Work](student-work/) | Submission area (private) |

## Quick Start Guide for Students

1. **Prerequisites**
   - Basic familiarity with Excel/Google Sheets
   - No prior programming experience required
   - Access to a computer with internet connection

2. **Required Software**
   - AntConc (free corpus analysis tool)
   - JASP (free statistical software)
   - Google account (for Colab notebooks)
   - Text editor (e.g., VS Code, Notepad++)

3. **Getting Started**
   - Review the [syllabus](syllabus/)
   - Check the [course schedule](syllabus/schedule.md)
   - Install required software (see [tools guide](resources/tools/))
   - Join the course communication channel

## Technical Requirements

- **Operating System**: Windows, macOS, or Linux
- **Memory**: 4GB RAM minimum (8GB recommended)
- **Storage**: 2GB free space for software and data
- **Internet**: Stable connection for online tools

## Course Structure

The course is organized into:
- **5 days** of intensive instruction
- **3 sessions per day** (morning and afternoon)
- **4 hands-on assignments**
- **1 final project**

## Contact Information

- **Email**: [instructor email]
- **Office Hours**: [schedule]
- **Course Website**: https://[username].github.io/Linguistic_Data_Analysis_I/

## Technical Notes

This repository uses Quarto for site generation with a hybrid rendering approach:
- **Primary**: Pre-render locally with `quarto render` and commit `docs/` folder
- **Fallback**: GitHub Actions automatically re-renders if source files change

The markdown files include Quarto-specific YAML headers and features (callout blocks, Mermaid diagrams). If you need Jekyll-compatible versions, use the conversion script in `/scripts/convert-to-jekyll.sh`.

See [RENDERING.md](RENDERING.md) for detailed information about the rendering strategy.

## License

Course materials are licensed under [specify license]. Please see individual resources for their specific licensing terms.