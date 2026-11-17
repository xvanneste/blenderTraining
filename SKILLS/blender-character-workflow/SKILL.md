---
name: blender-character-workflow
description: Build, fit, finish, rig, or animate a humanoid in Blender from front and profile references. Use for character proportions, continuous anatomy, garment and shoe fit, UVs, skinning, and walk cycles. Use another workflow for general Blender lessons or unrelated prop modeling.
---

# Blender character workflow

Preserve the user's reference images and approved Blender file. Work in a sibling version for each substantial change. Deliver the editable scene and show the exact area changed at a useful scale.

1. **Align the guides.** Match crown and floor, check common landmarks, and note where perspective or occlusion invalidates a direct correspondence. Display the guides on the two orthographic axes. Use them to constrain width, depth and landmarks.
2. **Start from suitable anatomy.** For a recognizable person, fit a continuous anatomical base with usable facial and joint topology, then refine the eyes, jaw and other identity cues in neutral lighting. When a base has related UVs, skeleton and weights, keep their vertex indices synchronized. Confirm permission and provenance before reusing source assets.
3. **Review form before presentation.** Compare front, profile and three-quarter views in clay. A silhouette hull can check overall proportions. It loses cheek, eye, finger and muscle structure and should not become the final face. Treat a projected texture as a material experiment, then verify the shape without it.
4. **Keep anatomy under clothing.** Garments, hair and shoes can be separate. Preserve the skin mesh at necks and ankles. Fit the shoe around the foot and inspect a cutaway. Check the cuff and tongue in a neutral view and again in a bent pose. For a cut made with a smooth Mask modifier, use interpolated signed weights across the entire edge span near the cut.
5. **Check the deliverable in Blender.** Reload the saved file, verify the packed maps and guides, and test weight continuity and motion on the edited parts. For a walk, plot or measure the evaluated foot in world space during stance, keep the support target fixed, and check penetration during swing. Review the exported clip for gait and the source scene for editability.

Read [the project case notes](references/case-study.md) when adapting this workflow, especially for driver preservation, foot contact tests and examples of useful failure checks.
