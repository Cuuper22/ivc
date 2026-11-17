# Reading task

Open only `blind_set.csv`. It has 240 lines, one per row: `item`, `object_kind`, `english`.

Each line is a proposed English reading of a short text on an ancient object of the named kind:
a personal seal, a ration or account tablet, a goods tag or sealing, a pot, a copper tablet, or another small object.

Grade each line:

- **sense**: it reads as something that kind of object would plausibly say: a name with house and title, an amount of goods, an ownership or office label.
- **odd**: parts make sense, something is off.
- **nonsense**: it does not read as anything that kind of object would say.

Grade every line on its own. Do not compare lines with each other.

Do not open any other file in this folder or in the repository.

Write your grades to `grades.csv` in this folder, with columns `item`, `grade`, `reason`: one row per item (240 rows), `grade` being exactly `sense`, `odd` or `nonsense`, and `reason` one short phrase.
