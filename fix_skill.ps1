# Fix non-ASCII bytes in ai4inv SKILL.md then restage and commit
$path = "skills\ai4inv-webinar-processor\SKILL.md"
$bytes = [System.IO.File]::ReadAllBytes($path)
$replacements = @(
    @(0x80, 0x94, [byte[]]@(0x20, 0x2D, 0x2D)),  # euro+rdquote -> ' --'
    @(0x80, 0x93, [byte[]]@(0x20, 0x2D, 0x2D)),  # euro+ldquote -> ' --'
    @(0x80, 0x92, [byte[]]@(0x27)),               # euro+rsquote -> '
    @(0x80, 0x99, [byte[]]@(0x28, 0x54, 0x4D, 0x29)) # euro+TM -> (TM)
)
# Single-byte replacements
$single = @{
    0x80 = [byte[]]@()
    0x85 = [byte[]]@(0x2E, 0x2E, 0x2E)
    0x91 = [byte[]]@(0x27)
    0x92 = [byte[]]@(0x27)
    0x93 = [byte[]]@(0x22)
    0x94 = [byte[]]@(0x22)
    0x95 = [byte[]]@(0x2D)
    0x96 = [byte[]]@(0x2D)
    0x97 = [byte[]]@(0x2D)
    0x99 = [byte[]]@(0x28, 0x54, 0x4D, 0x29)
    0xA0 = [byte[]]@(0x20)
}
# Convert to List for manipulation
$list = [System.Collections.Generic.List[byte]]$bytes
# Multi-byte pass
foreach ($r in $replacements) {
    $find1 = $r[0]; $find2 = $r[1]; $repl = $r[2]
    $i = 0
    while ($i -lt ($list.Count - 1)) {
        if ($list[$i] -eq $find1 -and $list[$i+1] -eq $find2) {
            $list.RemoveRange($i, 2)
            $list.InsertRange($i, $repl)
            $i += $repl.Count
        } else { $i++ }
    }
}
# Single-byte pass
$i = 0
while ($i -lt $list.Count) {
    if ($single.ContainsKey([int]$list[$i])) {
        $repl = $single[[int]$list[$i]]
        $list.RemoveAt($i)
        if ($repl.Count -gt 0) {
            $list.InsertRange($i, $repl)
            $i += $repl.Count
        }
    } else { $i++ }
}
[System.IO.File]::WriteAllBytes($path, $list.ToArray())
Write-Host "[FIXED] SKILL.md cleaned"
git add $path
Write-Host "[STAGED] SKILL.md restaged"
git commit -m "Daily commit: 2026-04-27 - fix non-ASCII chars, add new skills"
git push
Write-Host "[DONE] Commit and push complete"
