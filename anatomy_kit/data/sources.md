# Sources for anatomy_kit data

## Anthropometry

- Winter, D. A. *Biomechanics and Motor Control of Human Movement*, 4th ed.
  Wiley, 2009. Segment mass fractions, COM locations, and length fractions used
  in `segments_winter.json`.
- Module 1 Appendix of this course cites Winter for forearm+hand regression
  fractions used in torque examples (`m_s = 0.022 M`, `r_s ≈ 0.43 ℓ_fa`).

## Gait kinematics

- Winter, D. A. *The Biomechanics and Motor Control of Human Gait*, Waterloo
  Biomechanics (representative sagittal means).
- Perry, J. & Burnfield, J. *Gait Analysis: Normal and Pathological Function*
  (event definitions: IC, midstance, toe-off, midswing).
- Course Module 8 timeline: stance ≈ 60–62% of stride for normal walking.

Values in `gait_angles_deg.json` are **teaching-grade rounded means** for
sagittal hip/knee/ankle at named events, not subject-specific lab data.
Captions should say “typical adult means” when absolute angles matter.

## COP path

- Teaching schematic of typical plantar center-of-pressure progression in
  level walking: heel → lateral midfoot → medial forefoot / hallux.
  Normalized coordinates in `cop_plantar_path.json` are schematic, not a
  single published force-plate trace.
