
# Scenes

Basic scenes are implemented. But we need some kind of "sub-scenes", scenes that
happen within another scene, which can transition either to a new scene or a new
subscene. Subscenes can come in two forms:

* A conditional paragraph in the main scene's content
* A subscene happening upon selecting a choice, which will update the main scene's
content and may deplete 0, one or more choices (If choice-based scene rather than
rare input based)