# Map

What we currently act on, the live leads in order, and what each one says we should see next. `measured` = a number came out of data. `guess` = we act as if.

## Beliefs

- `measured` Seals found in the same room at Mohenjo-daro, within 3 ft of depth, share an uncommon sign in the middle of the text about 7 times as often as chance (5 pairs against 0.73). First and last signs show no excess.
- `guess` A seal text has three parts: a citywide opening, a middle that belongs to the people of one room (a name or family element), a citywide closing.
- `measured` Among seals that close with the jar sign (Lipi 740), house-mates share the sign right before the jar in 15 pairs against 9.3 by chance, often a rare one, and sometimes the whole last three signs.
- `guess` The sign or pair right before the closing jar is a house or family name; the jar is the "of / belonging to" ending.
- `measured` House-mates share the animal on the seal a little more often than chance (12.5% against 11.0%).
- `guess` The animal marks a larger group (clan, guild, office); the middle of the text marks the household or person inside it.
- `measured` On two-sided tablets one face is the cup sign plus 2, 3 or 4 long strokes (107 / 157 / 123 objects); cup plus 1 stroke occurs 4 times. Tablet area falls about 8% per extra stroke within one tablet format.
- `guess` Cup + strokes is a quantity field (a share, grade or measure) and the other face says who or what it is for.
- `measured` 12 of 17 round seals found in the Gulf, Mesopotamia and Iran carry the man sign or the twin-men sign (Lipi 090 / 091); these signs are rare at home.
- `guess` The round seals abroad write foreign names with Indus signs, and the man sign there is a name marker.

- `measured` Lipi sign numbers are Wells numbers, so every sign now has a described shape (`work_data/sign_shapes.csv`). Short strokes run 1 to 8 and full-height strokes 1 to 5 as two separate series.
- `guess` Two stroke heights are two counting systems for two kinds of thing.
- `measured` After `person-with-two-loads (154/158)` + `leaf-on-tree (806)` the next stored sign is one of 11 A-shaped variants (465-475): 23 of 23 on held-back Harappa texts, 6 of 6 at other sites.
- `measured` The A-shape is one sign with a comb of about 3 to 8 ticks at its foot, sitting in the count slot before leaf-on-tree (806); the load-carrier follows only then (36 of 36). Harappa's granary area holds 11 of 23 of these objects.
- `guess` READING: `[A with n ticks] [leaf-on-tree] [load-carrier]` = "n loads of crop, carried" : a counted load tag. Leaf-on-tree (806) is a crop or produce word; the A-comb is a load count; the carrier sign is the porter or the load. H-152, H-670, H-681, M-1986 read whole this way.

- `measured` Seal texts end in one of a handful of closing signs (jar, spear, plain person, comb, load-carrier). The mix of closers is the same at every site. Seal size goes with the closer: person 738 mm2, jar 645, spear 633, carrier 495, comb 420 (median face area).
- `guess` The closing sign is the owner's class or office, the same system across the whole civilisation, and seal size follows rank. The slot before it is the house name. A seal reads: [opener] [who] [house] [class].

## Live leads, in order

1. Name slot. `guess` The slot right before the closing jar holds a house or family name. Next: build the list of pre-jar signs and pre-jar pairs with the houses they belong to; check whether one house keeps one pre-jar sign across depth (a family over generations); check the same slot before the other closing signs.
2. Cup tablets as accounts. `guess` Front = who or what, back = how much. Next: group fronts by their last sign and see whether each group keeps to one stroke count; tie tablet findspots at Harappa to what was made or stored there.
3. Seals abroad. `guess` Foreign names spelled in Indus signs. Next: line the round-seal texts up against each other for shared pieces in shared positions.
4. Load tags. `guess` 806 is a crop. Next: every other sign that takes a count before it and a carrier after it is another commodity; list them. Tick counts on the A against the stroke count written before the phrase on seals.
5. Endings grammar from the sweep: two signs that govern how a text closes (78.7% top-3 on held-back texts against 17.7%), the closing cap `060-920` (64 of 65 at the end), closing versus open signs after the two-stroke opener (22 of 23 against 0 of 12).
6. The rest of `sweep/LEADS.md`.
