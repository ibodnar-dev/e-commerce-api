# E-Commerce API - Project Instructions

## Project Structure
This is the main CLAUDE.md for this e-commerce API project. Documentation is organized in subdirectories:

- `.claude/project/` - General project guidelines and conventions
- `.claude/domain/` - Domain models, database schemas, and architecture documentation

## Project Guidelines
Always follow the conventions in:
- **General Guidelines**: `.claude/project/general-guidelines.md` - Code formatting and file conventions

## Domain Documentation
When working on features, always reference the relevant domain documentation:

- **Database Schema**: `.claude/domain/db-entities.md` - Complete product catalog schema including:
  - Products (simple and variable types)
  - Product variants with attributes (size, color, etc.)
  - Inventory management
  - Attribute system for product options

## Development Guidelines
- Follow the database schema defined in `db-entities.md` when creating entities and repositories
- Maintain separation between simple products (single SKU) and variable products (multiple variants)
- Always validate business rules as documented in the domain files
