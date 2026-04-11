@echo off
echo ============================================================
echo Committing 2026.03.12 evening session - WordPress Skills
echo ============================================================

echo.
echo [1/2] Committing Dex-MickP (CEDRIC_MEMORY + CHANGELOG)...
cd /d "C:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP"
git add CEDRIC_MEMORY.md CHANGELOG.md
git commit -m "2026.03.12 evening - WordPress publisher skills + session memory update

- Added portfolio-post-creator and wordpress-post-publisher to skills inventory
- Session summary 2026.03.12 added (WordPress automation architecture + vault deploy)
- Changelog entry added
- Skills inventory now 13 skills across both vaults"
git push
echo Dex-MickP done.

echo.
echo [2/2] Committing Mick's Vault (new skills + CHANGELOG)...
cd /d "C:\Vaults\Mick's Vault"
git add .claude\skills\portfolio-post-creator\ .claude\skills\wordpress-post-publisher\ .claude\CHANGELOG.md
git commit -m "2026.03.12 - Add portfolio-post-creator and wordpress-post-publisher skills

Two new skills for WordPress post automation:
- portfolio-post-creator: HTML post generator for 4 portfolio pages, all 6 post types
- wordpress-post-publisher: Generic WP REST API draft publisher
- Separation of concerns design, self-improving feedback loop
- Poster Pete (Editor) credentials architecture documented
- CHANGELOG updated"
git push
echo Mick's Vault done.

echo.
echo ============================================================
echo All commits complete. Press any key to close.
echo ============================================================
pause
