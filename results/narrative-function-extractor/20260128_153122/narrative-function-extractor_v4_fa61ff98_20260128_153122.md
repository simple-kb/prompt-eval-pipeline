# Evaluation Report: narrative-function-extractor_v4

**Run ID:** fa61ff98
**Model:** claude-opus-4-5-20251101
**Date:** 2026-01-28 15:29:28

## Summary

| Metric | Value |
|--------|-------|
| Total Tests | 3 |
| Passed | 1 |
| Failed | 2 |
| Pass Rate | 33.3% |
| Avg Latency | 37877 ms |
| Total Tokens | 9361 |

## Results

| Test Case | Passed | Latency (ms) | Metrics |
|-----------|--------|--------------|---------|
| Les Oies sauvages | ✅ | 32427 | contains=1.00 |
| Morozko | ❌ | 37390 | contains=0.00 |
| Vassilissa-la-très-belle | ❌ | 43812 | contains=0.00 |

## Test Details

### Les Oies sauvages ✅

**System Prompt:**
```
(Pas encore défini)

<rules>
- Avant de faire quoi que ce soit, vérifie que tu as accès aux 31 fichiers .md, décrivant les fonctions narratives.
- Si tu n'as pas accès aux 31 fichiers .md, génère simplement un avertissement et arrète.
- Chacun des 31 fichiers .md décrit une fonction narrative.
- Pour chaque fonction narrative, le "nom de la fonction" est défini dans son fichier .md. Sois très précis lorsque tu références les noms des fonctions
- Pour qu'une fonction narrative soit correctement identifiée dans le cadre de Propp, elle devrait apparaître dans sa position canonique par rapport aux autres fonctions présentes dans le conte. Une fonction apparaissant "dans le désordre" indiquerait soit un élément structurel différent, soit une déviation nécessitant une explication spéciale, soit potentiellement une mauvaise identification de la fonction elle-même.
</rules>

<skills>
- (Pas encore défini)
</skills>

<thinking_process>
Lis le conte populaire une première fois dans son ensemble pour saisir l'intrigue et le sens complet.
Puis itère à travers chacun des 31 fichiers .md.
Pour chacune de ces fonctions narratives, il faut:
 - Evaluer si la fonction narrative d'applique ou non au conte. 
 Attention, la fonction ne s'applique pas si elle apparaît au mauvais moment dans le conte. 
 Le texte auquel s'applique la fonction doit apparaître dans sa position canonique par rapport aux autres fonctions présentes dans le conte.
 - Il faut donc relire les fonctions narratives déjà identifiées, et vérifier que cette nouvelle fonction narrative intervient après !
 - Justifier cette évaluation
 - Attribuer un niveau de confiance (de 0 à 1) à l'évaluation.
</thinking_process>
```

**Input:**
```
Considère le conte populaire suivant:
"""
Des parents villageois qui s'en vont au travail (ou à la foire) confient leur très jeune fils à la garde de leur sœur, une fillette. Celle-ci ne tarde pas à relâcher sa surveillance et des oies sauvages (ou des cygnes) se saisissent du bébé assis sur l'herbe et l'emportent. La fillette part à leur recherche et rencontre successivement en chemin un four à pain, un pommier sauvage et une rivière de lait aux berges de kissel[3]. Chacun d'eux lui propose avant de la guider, qui un petit pain de seigle, qui une pomme aigrelette, qui du kissel arrosé de lait, mais elle dédaigne toutes ces offres. C'est un hérisson (qu'elle a, par prudence, évité de maltraiter) qui l'oriente finalement vers l'endroit où les oies sauvages ont déposé son petit frère : il s'agit de l'isba de Baba Yaga, où l'enfant joue avec des pommes d'or. En cachette, la fillette parvient à saisir son petit frère et à s'enfuir avec lui, mais les oies sauvages la repèrent bientôt et se mettent à tourner, menaçantes, au-dessus d'elle. Elle croise alors à nouveau, dans l'ordre inverse, la rivière, le pommier et le four à pain, desquels elle implore successivement de l'aide pour se cacher. Chacun d'eux le fera, mais seulement après qu'elle aura accepté leur proposition initiale : dans son affolement, elle n'a garde cette fois de jouer la dégoûtée. Ayant échappé aux oies, la fillette rejoint sa maison avec son petit frère au moment même où rentrent ses parents.

"""

Identifie les fonctions narratives.

La réponse doit contenir 2 parties...

Partie 1 est le tableau détaillé:
* chaque ligne est la fonction candidate. (il y aura donc 31 lignes)
* colonne 1: nom de la fonction
* colonne 2: justification (si elle s'applique ou non).
Si le score de confiance est entre 0.8 et 0.89, alors tu dois être très prudent, reconsidérer le score et fournir plus de justifications.
* colonne 3: applicable. Ceci doit contenir le score de confiance que tu viens de calculer et réévaluer.

Partie 2 est la séquence résultante:
Lis chaque ligne du tableau détaillé.
Garde uniquement les fonctions avec un score de confiance supérieur ou égal à 0.85.
Concatène ces numéros de fonctions avec un séparateur virgule.
Écris cette séquence concaténée.

```

**Output:**
```
# Analyse des fonctions narratives du conte "Les oies sauvages"

## Partie 1 : Tableau détaillé

| Nom de la fonction | Justification | Score de confiance |
|---|---|---|
| 01. Éloignement | Les parents partent au travail (ou à la foire), laissant les enfants seuls. C'est une forme classique β¹ d'éloignement de la génération plus âgée. | 0.95 |
| 02. Interdiction | L'interdiction est implicite dans la consigne de "garder" le petit frère. La fillette reçoit la responsabilité de surveiller l'enfant, ce qui implique de ne pas le perdre de vue. Forme γ¹ atténuée. | 0.85 |
| 03. Transgression | La fillette "relâche sa surveillance", violant ainsi l'interdiction implicite de veiller sur son frère. Correspond à δ. | 0.90 |
| 04. Interrogation | Aucune tentative de reconnaissance par l'agresseur n'est mentionnée. Les oies agissent directement sans chercher d'information. | 0.10 |
| 05. Délation | Aucune information n'est transmise à l'agresseur. Les oies trouvent l'enfant sans aide extérieure. | 0.10 |
| 06. Tromperie | Les oies n'utilisent pas de tromperie pour s'emparer de l'enfant. Elles agissent par force directe. | 0.10 |
| 07. Complicité | La victime ne se laisse pas tromper volontairement. L'enlèvement est subi passivement. | 0.10 |
| 08. Méfait (ou Manque) | Les oies sauvages enlèvent le petit frère (A¹). C'est un méfait classique d'enlèvement qui déclenche l'action du conte. | 0.95 |
| 09. Appel | Le malheur (enlèvement) est constaté par la fillette qui décide de partir à la recherche de son frère. Forme B⁴ où le malheur provoque directement le départ. | 0.90 |
| 10. Entreprise réparatrice | La fillette décide de partir à la recherche de son frère. C'est une décision volontaire de contre-action (C). | 0.90 |
| 11. Départ | La fillette quitte la maison pour chercher son frère. Départ classique (↑) du héros-quêteur. | 0.95 |
| 12. Première fonction du donateur | Le four, le pommier et la rivière proposent chacun quelque chose à la fillette (D¹ - test sous forme d'offre). Le hérisson représente aussi un donateur potentiel (d⁷ - possibilité de rendre service en ne le maltraitant pas). | 0.90 |
| 13. Réaction du héros | La fillette refuse les offres du four, du pommier et de la rivière (réaction négative E¹ neg.). Cependant, elle évite de maltraiter le hérisson (réaction positive). | 0.90 |
| 14. Réception de l'objet magique | Le hérisson indique le chemin vers l'isba de Baba Yaga (F² - l'agent/information est indiqué). Ce n'est pas un objet magique au sens strict, mais une aide cruciale. | 0.85 |
| 15. Déplacement | La fillette est guidée par le hérisson vers l'isba de Baba Yaga (G⁴ - la route lui est montrée). | 0.90 |
| 16. Combat | Aucun combat direct entre la fillette et un agresseur. Elle récupère son frère en cachette. | 0.10 |
| 17. Marque | La fillette ne reçoit aucune marque distinctive. | 0.05 |
| 18. Victoire | Pas de victoire au combat. La récupération du frère se fait par ruse/discrétion, pas par affrontement. | 0.15 |
| 19. Réparation | La fillette récupère son petit frère (K¹ - l'objet de la quête est saisi par la ruse). Le méfait initial est réparé. | 0.95 |
| 20. Retour | La fillette s'enfuit avec son frère pour rentrer chez elle (↓). | 0.95 |
| 21. Poursuite | Les oies sauvages repèrent la fillette et se mettent à tourner menaçantes au-dessus d'elle (Pr¹ - le poursuivant vole après le héros). | 0.95 |
| 22. Secours | La rivière, le pommier et le four cachent successivement la fillette (Rs⁴ - le héros se cache pendant sa fuite). Cette fois, elle accepte leurs offres et ils l'aident. | 0.95 |
| 23. Arrivée incognito | La fillette ne revient pas incognito. Elle rentre simplement chez elle. | 0.10 |
| 24. Imposture | Aucun faux héros ne présente de prétentions. | 0.05 |
| 25. Tâche difficile | Aucune tâche difficile n'est proposée à la fillette. | 0.10 |
| 26. Accomplissement | Pas de tâche à accomplir. | 0.10 |
| 27. Reconnaissance | Pas de reconnaissance formelle du héros. | 0.10 |
| 28. Découverte | Pas de faux héros à démasquer. | 0.05 |
| 29. Transfiguration | La fillette ne reçoit pas de nouvelle apparence. | 0.05 |
| 30. Châtiment | Les oies/Baba Yaga ne sont pas punies. | 0.10 |
| 31. Mariage | Pas de mariage. Le conte se termine par le retour au foyer au moment où les parents rentrent. | 0.05 |

---

## Partie 2 : Séquence résultante

Fonctions avec score ≥ 0.85 :

**01, 02, 03, 08, 09, 10, 11, 12, 13, 14, 15, 19, 20, 21, 22**
```

**Metrics:** {'contains': 1.0}

### Morozko ❌

**System Prompt:**
```
(Pas encore défini)

<rules>
- Avant de faire quoi que ce soit, vérifie que tu as accès aux 31 fichiers .md, décrivant les fonctions narratives.
- Si tu n'as pas accès aux 31 fichiers .md, génère simplement un avertissement et arrète.
- Chacun des 31 fichiers .md décrit une fonction narrative.
- Pour chaque fonction narrative, le "nom de la fonction" est défini dans son fichier .md. Sois très précis lorsque tu références les noms des fonctions
- Pour qu'une fonction narrative soit correctement identifiée dans le cadre de Propp, elle devrait apparaître dans sa position canonique par rapport aux autres fonctions présentes dans le conte. Une fonction apparaissant "dans le désordre" indiquerait soit un élément structurel différent, soit une déviation nécessitant une explication spéciale, soit potentiellement une mauvaise identification de la fonction elle-même.
</rules>

<skills>
- (Pas encore défini)
</skills>

<thinking_process>
Lis le conte populaire une première fois dans son ensemble pour saisir l'intrigue et le sens complet.
Puis itère à travers chacun des 31 fichiers .md.
Pour chacune de ces fonctions narratives, il faut:
 - Evaluer si la fonction narrative d'applique ou non au conte. 
 Attention, la fonction ne s'applique pas si elle apparaît au mauvais moment dans le conte. 
 Le texte auquel s'applique la fonction doit apparaître dans sa position canonique par rapport aux autres fonctions présentes dans le conte.
 - Il faut donc relire les fonctions narratives déjà identifiées, et vérifier que cette nouvelle fonction narrative intervient après !
 - Justifier cette évaluation
 - Attribuer un niveau de confiance (de 0 à 1) à l'évaluation.
</thinking_process>
```

**Input:**
```
Considère le conte populaire suivant:
"""
Un couple de vieux a trois filles. La vieille n'aime pas l'aînée, Martha, qui est en réalité sa belle-fille, et elle lui rend la vie pénible. Comme le couple songe à marier ses filles, la vieille cherche à en profiter pour se débarrasser de l'aînée en la mariant au Gel, malgré ses pleurs, en le lui présentant comme un riche et beau parti. Le vieux est contraint d'abandonner sa fille au pied d'un grand pin. Arrive le Gel (Morozko) « sautant de sapin en sapin », qui lui demande à plusieurs reprises si elle a chaud. Bien que glacée, elle affirme que oui et lui répond tendrement. Le Gel s'attendrit, la couvre de fourrures somptueuses et la renvoie chez elle sur un traîneau avec de riches présents. Stupéfaite, la vieille décide d'envoyer à leur tour ses deux filles se fiancer à Morozko pour qu'il les comble de cadeaux. Laissées au pied du pin, celles-ci maudissent le froid et leur promis qui ne vient pas. Arrive le Gel qui leur demande si elles ont chaud, mais elles l'envoient à tous les diables, et meurent pétrifiées de froid. Le lendemain, le vieux ramène à la vieille ses deux filles mortes. La vieille entre en rage, mais est contrainte de faire la paix avec sa belle-fille, qui épousera finalement un voisin.

"""

Identifie les fonctions narratives.

La réponse doit contenir 2 parties...

Partie 1 est le tableau détaillé:
* chaque ligne est la fonction candidate. (il y aura donc 31 lignes)
* colonne 1: nom de la fonction
* colonne 2: justification (si elle s'applique ou non).
Si le score de confiance est entre 0.8 et 0.89, alors tu dois être très prudent, reconsidérer le score et fournir plus de justifications.
* colonne 3: applicable. Ceci doit contenir le score de confiance que tu viens de calculer et réévaluer.

Partie 2 est la séquence résultante:
Lis chaque ligne du tableau détaillé.
Garde uniquement les fonctions avec un score de confiance supérieur ou égal à 0.85.
Concatène ces numéros de fonctions avec un séparateur virgule.
Écris cette séquence concaténée.

```

**Output:**
```
# Analyse des fonctions narratives du conte "Morozko"

## Partie 1 : Tableau détaillé

| Nom de la fonction | Justification | Score de confiance |
|---|---|---|
| 01. Éloignement | Le vieux est contraint d'abandonner Martha au pied du pin, ce qui constitue un éloignement de la maison familiale. C'est un membre de la génération plus âgée qui emmène l'héroïne loin du foyer (β¹). | 0.95 |
| 02. Interdiction | Aucune interdiction explicite n'est formulée dans le conte. La situation initiale présente la maltraitance de Martha, mais pas d'interdiction au sens de Propp. | 0.10 |
| 03. Transgression | Sans interdiction préalable, il n'y a pas de transgression à identifier. | 0.05 |
| 04. Interrogation | Le Gel interroge Martha à plusieurs reprises : "as-tu chaud ?" Cette interrogation sert à tester la victime, mais ce n'est pas une reconnaissance au sens de l'agresseur cherchant des informations sur sa victime. Le Gel n'est pas vraiment un agresseur ici. | 0.25 |
| 05. Délation | Aucune information n'est transmise à un agresseur sur la victime. | 0.05 |
| 06. Tromperie | La vieille trompe Martha en lui présentant le Gel comme "un riche et beau parti" pour la marier, alors qu'elle cherche en réalité à s'en débarrasser. C'est une forme de persuasion trompeuse (η¹). | 0.90 |
| 07. Complicité | Martha, malgré ses pleurs, est contrainte d'accepter la situation. Elle ne se laisse pas vraiment tromper volontairement, elle est forcée. La complicité au sens de Propp implique que la victime aide involontairement son ennemi en acceptant les persuasions. Ici, c'est plutôt une soumission forcée. | 0.40 |
| 08. Méfait (ou Manque) | La marâtre cherche à se débarrasser de Martha en l'envoyant au Gel pour qu'elle meure de froid. C'est une forme d'expulsion (A⁹) combinée avec une tentative de meurtre indirect (A¹³). Le méfait est clairement établi. | 0.95 |
| 09. Appel | Martha est transportée loin de la maison (B⁵) - le père l'emmène dans la forêt. C'est la forme typique du héros-victime banni qui est transporté. | 0.90 |
| 10. Entreprise réparatrice | Martha ne décide pas d'une contre-action. Elle est une héroïne-victime passive, pas une quêteuse. Cette fonction est absente pour ce type de héros. | 0.10 |
| 11. Départ | Martha quitte la maison, emmenée par son père au pied du pin. C'est le départ du héros-victime (↑). | 0.90 |
| 12. Première fonction du donateur | Le Gel met Martha à l'épreuve en lui demandant plusieurs fois si elle a chaud (D¹). C'est un test de caractère et d'endurance. Elle doit répondre correctement malgré le froid glacial. | 0.95 |
| 13. Réaction du héros | Martha répond positivement et tendrement au Gel malgré le froid, affirmant qu'elle a chaud (E¹). Elle réussit l'épreuve par sa politesse et sa douceur. | 0.95 |
| 14. Réception de l'objet magique | Le Gel couvre Martha de fourrures somptueuses et lui donne de riches présents, puis un traîneau (F¹). Ce sont des dons directs en récompense de sa réussite à l'épreuve. | 0.92 |
| 15. Déplacement | Martha est renvoyée chez elle sur un traîneau. C'est un transport (G²), mais c'est plutôt un retour qu'un déplacement vers l'objet de quête. | 0.30 |
| 16. Combat | Aucun combat direct entre héros et agresseur. | 0.05 |
| 17. Marque | Martha n'est pas marquée physiquement. | 0.05 |
| 18. Victoire | Il n'y a pas de victoire au combat. La "victoire" de Martha est sa survie et ses récompenses, mais ce n'est pas la fonction XVIII au sens strict. | 0.15 |
| 19. Réparation | Le méfait initial (l'expulsion pour mourir) est réparé : Martha revient vivante, riche, avec des fourrures et des présents. Le manque/méfait est liquidé (K). | 0.90 |
| 20. Retour | Martha retourne chez elle sur le traîneau donné par le Gel (↓). | 0.92 |
| 21. Poursuite | Aucune poursuite du héros. | 0.05 |
| 22. Secours | Pas de secours contre une poursuite. | 0.05 |
| 23. Arrivée incognito | Martha n'arrive pas incognito, elle revient ouvertement avec ses richesses. | 0.05 |
| 24. Imposture | Les deux filles de la marâtre tentent d'obtenir les mêmes récompenses en se faisant passer pour des prétendantes dignes du Gel. C'est une forme de prétention non fondée (L). | 0.75 |
| 25. Tâche difficile | Aucune tâche difficile n'est proposée au héros après son retour. | 0.10 |
| 26. Accomplissement | Pas de tâche à accomplir. | 0.05 |
| 27. Reconnaissance | Martha est reconnue implicitement par sa transformation sociale (richesse), mais ce n'est pas une reconnaissance au sens de Propp (par une marque ou après une séparation). | 0.20 |
| 28. Découverte | Les fausses héroïnes (les deux sœurs) sont démasquées par leur échec : elles meurent de froid, révélant leur indignité. Leur comportement grossier les a trahies. | 0.85 |
| 29. Transfiguration | Martha ne reçoit pas une nouvelle apparence physique au sens magique. Ses richesses changent son statut social mais pas sa forme. | 0.25 |
| 30. Châtiment | Les deux sœurs meurent pétrifiées de froid - c'est leur châtiment pour leur comportement. La marâtre est "contrainte de faire la paix" - forme atténuée de châtiment. | 0.88 |
| 31. Mariage | Martha épouse finalement un voisin. C'est un mariage sans royaume (W*). | 0.95 |

## Partie 2 : Séquence résultante

En conservant uniquement les fonctions avec un score ≥ 0.85 :

**01, 06, 08, 09, 11, 12, 13, 14, 19, 20, 28, 30, 31**
```

**Metrics:** {'contains': 0.0}

### Vassilissa-la-très-belle ❌

**System Prompt:**
```
(Pas encore défini)

<rules>
- Avant de faire quoi que ce soit, vérifie que tu as accès aux 31 fichiers .md, décrivant les fonctions narratives.
- Si tu n'as pas accès aux 31 fichiers .md, génère simplement un avertissement et arrète.
- Chacun des 31 fichiers .md décrit une fonction narrative.
- Pour chaque fonction narrative, le "nom de la fonction" est défini dans son fichier .md. Sois très précis lorsque tu références les noms des fonctions
- Pour qu'une fonction narrative soit correctement identifiée dans le cadre de Propp, elle devrait apparaître dans sa position canonique par rapport aux autres fonctions présentes dans le conte. Une fonction apparaissant "dans le désordre" indiquerait soit un élément structurel différent, soit une déviation nécessitant une explication spéciale, soit potentiellement une mauvaise identification de la fonction elle-même.
</rules>

<skills>
- (Pas encore défini)
</skills>

<thinking_process>
Lis le conte populaire une première fois dans son ensemble pour saisir l'intrigue et le sens complet.
Puis itère à travers chacun des 31 fichiers .md.
Pour chacune de ces fonctions narratives, il faut:
 - Evaluer si la fonction narrative d'applique ou non au conte. 
 Attention, la fonction ne s'applique pas si elle apparaît au mauvais moment dans le conte. 
 Le texte auquel s'applique la fonction doit apparaître dans sa position canonique par rapport aux autres fonctions présentes dans le conte.
 - Il faut donc relire les fonctions narratives déjà identifiées, et vérifier que cette nouvelle fonction narrative intervient après !
 - Justifier cette évaluation
 - Attribuer un niveau de confiance (de 0 à 1) à l'évaluation.
</thinking_process>
```

**Input:**
```
Considère le conte populaire suivant:
"""
Vassilissa est la fille unique d'un marchand veuf. Avant de mourir, sa mère lui a confié une poupée en lui recommandant de la garder précieusement avec elle, de ne la montrer à personne et de lui donner à manger lorsqu'elle-même aura besoin d'aide. Le marchand se remarie avec une veuve qui a déjà deux filles, lesquelles se mettent à jalouser et à tourmenter Vassilissa. Celle-ci, en cachette, raconte ses malheurs à la poupée, qui la conseille et l'aide en réalisant les travaux pénibles à sa place. Un jour, alors que le marchand est parti pour un long voyage, la marâtre envoie Vassilissa chez la sorcière cannibale Baba Yaga sous le prétexte de lui demander du feu, que ses filles ont laissé s'éteindre. La poupée la réconforte et lui recommande de l'emporter avec elle. Chemin faisant, Vassilissa rencontre successivement trois cavaliers, l'un tout blanc à l'aube, le second tout rouge à l'aurore ; elle croise le troisième, tout noir, alors qu'elle est parvenue à la clairière où se dresse la hutte de Baba Yaga et que la nuit tombe. L'endroit est particulièrement sinistre, la maison étant faite d'ossements, ornée de crânes portant des yeux brillant dans la nuit, et le cadenas étant figuré par une bouche prête à mordre. Arrive, voyageant dans les airs dans son mortier, la Baba Yaga, qui déclare sentir une odeur de chair humaine. Tremblante, Vassilissa se découvre et explique le motif de sa visite. Baba Yaga, qui indique au passage connaître les filles de la marâtre, la prend alors à son service, et lui ordonne d'abord de lui servir tout ce qui peut se manger et se boire dans la maison : elle dévore tout, ne laissant que quelques restes à la jeune fille. Avant de se coucher, elle lui annonce que le lendemain, en son absence, elle devra tout ranger, nettoyer, et trier un boisseau de blé grain par grain. La poupée, à qui Vassilissa a donné les restes et raconté sa peine, la réconforte, l'assurant que tout ira bien. Le lendemain, le travail se fait en effet tout seul, grâce à la poupée. A la nuit tombée, Baba Yaga est de retour et ne voit rien à redire. Elle appelle alors ses serviteurs pour moudre le blé, et trois paires de bras apparaissent et emportent le grain. Avant de se coucher, elle annonce à Vassilissa que le lendemain, en plus du travail effectué ce jour-là, elle devra trier un boisseau de graines de pavot, sans quoi elle sera dévorée. Encore une fois, la poupée lui conseille de prier et d'aller dormir tranquillement, demain étant un autre jour. Tout se passe de la même façon que la veille, et les trois paires de bras emportent les graines de pavot pour en extraire l'huile. Vassilissa s'enhardit à demander à la sorcière qui sont les trois cavaliers, et celle-ci lui répond qu'il s'agit de son jour clair, de son soleil ardent et de sa sombre nuit. La jeune fille s'abstient cependant prudemment d'en demander davantage à propos des trois paires de bras, et Baba Yaga l'approuve de ne poser des questions que sur ce qui se passe à l'extérieur, et non à l'intérieur. Toutefois, lorsque Vassilissa lui avoue qu'elle est aidée dans ses tâches par la bénédiction maternelle, la sorcière, irritée, la jette dehors, ne voulant « pas de bénis chez elle », mais non sans lui donner malgré tout un crâne aux yeux ardents planté sur un bâton, puisque les filles de la marâtre réclamaient du feu. Les yeux du crâne éclairent le chemin à travers la forêt que Vassilissa retraverse de nuit ; elle chemine encore un jour, puis veut jeter le crâne, pensant que les deux filles auront trouvé du feu entretemps, mais le crâne lui-même lui ordonne de n'en rien faire et de le porter jusque chez la marâtre. Lorsqu'elle arrive à la maison, plongée dans le noir, les yeux du crâne se fixent sur la marâtre et ses filles, les poursuivant partout et finissant par les consumer. Vassilissa enterre le crâne, ferme la maison et s'en va à la ville, où une vieille femme la recueille en attendant le retour de son père. La jeune fille, toujours aidée par sa poupée, se met à tisser une toile de lin extraordinairement légère et solide, et propose à la vieille d'aller la vendre au marché, mais celle-ci est d'avis qu'une telle toile ne peut qu'être offerte au tsar, ce qu'elle fait, recevant des cadeaux en échange. Le tsar veut faire couper des chemises dans la toile, mais aucun tailleur n'y parvient. Il envoie alors chercher la vieille, qui l'informe que c'est sa fille adoptive qui a tissé la toile. Le tsar ordonne que celle-ci couse elle-même les chemises. Vassilissa s'exécute, et se rend au palais pour livrer son travail, soigneusement vêtue et apprêtée : le tsar tombe immédiatement amoureux d'elle et l'épouse. Le père de Vassilissa revient de voyage, découvre le bonheur de sa fille et reste vivre auprès d'elle, ainsi que la vieille. Vassilissa, devenue tsarine, gardera toute sa vie sa poupée sur elle, dans sa poche. 

"""

Identifie les fonctions narratives.

La réponse doit contenir 2 parties...

Partie 1 est le tableau détaillé:
* chaque ligne est la fonction candidate. (il y aura donc 31 lignes)
* colonne 1: nom de la fonction
* colonne 2: justification (si elle s'applique ou non).
Si le score de confiance est entre 0.8 et 0.89, alors tu dois être très prudent, reconsidérer le score et fournir plus de justifications.
* colonne 3: applicable. Ceci doit contenir le score de confiance que tu viens de calculer et réévaluer.

Partie 2 est la séquence résultante:
Lis chaque ligne du tableau détaillé.
Garde uniquement les fonctions avec un score de confiance supérieur ou égal à 0.85.
Concatène ces numéros de fonctions avec un séparateur virgule.
Écris cette séquence concaténée.

```

**Output:**
```
# Analyse des fonctions narratives de "Vassilissa la Belle"

## Partie 1 : Tableau détaillé

| Nom de la fonction | Justification | Score de confiance |
|---|---|---|
| 01. Éloignement | La mère meurt (β²) - forme intensifiée d'éloignement. Plus tard, le père part pour un long voyage (β¹). Ces deux éloignements sont clairement présents au début du conte. | 0.95 |
| 02. Interdiction | La mère donne des instructions à Vassilissa : garder la poupée précieusement, ne la montrer à personne, lui donner à manger quand elle aura besoin d'aide. Ce sont des ordres/conseils (γ²) plutôt qu'une interdiction classique, mais ils fonctionnent comme tels. | 0.85 |
| 03. Transgression | Il n'y a pas de transgression claire de l'interdiction maternelle. Vassilissa suit fidèlement les conseils de sa mère tout au long du conte. La transgression n'est pas présente. | 0.10 |
| 04. Interrogation | Baba Yaga interroge Vassilissa sur sa présence ("sent une odeur de chair humaine", Vassilissa doit s'expliquer). Plus tard, Baba Yaga découvre que Vassilissa est aidée par "la bénédiction maternelle". Cependant, c'est Vassilissa qui pose des questions, pas l'agresseur qui fait de la reconnaissance. | 0.40 |
| 05. Délation | Vassilissa avoue à Baba Yaga qu'elle est aidée par la bénédiction maternelle. C'est une forme de délation involontaire (ζ¹). | 0.75 |
| 06. Tromperie | La marâtre envoie Vassilissa chez Baba Yaga sous le prétexte de demander du feu, sachant que c'est une sorcière cannibale. C'est une tromperie par persuasion (η¹) - un faux prétexte pour envoyer la victime à la mort. | 0.95 |
| 07. Complicité | Vassilissa accepte d'aller chez Baba Yaga, se laissant tromper par le prétexte du feu (θ¹). Elle obéit à l'ordre de la marâtre. | 0.90 |
| 08. Méfait (ou Manque) | La marâtre et ses filles tourmentent Vassilissa (A¹⁸ - tourmente). L'envoi chez Baba Yaga constitue une tentative de meurtre indirect (A¹³). De plus, il y a un manque initial : Vassilissa est orpheline de mère et maltraitée. | 0.95 |
| 09. Appel | Le malheur est rendu public par l'envoi de Vassilissa chez Baba Yaga. Elle est envoyée directement (B²) par la marâtre. C'est un héros-victime qui est transporté vers le danger (B⁵). | 0.90 |
| 10. Entreprise réparatrice | Vassilissa ne décide pas vraiment d'une contre-action volontaire. Elle est envoyée et obéit. La poupée la réconforte mais il n'y a pas de décision héroïque de contre-action. Cette fonction est typique des héros-quêteurs, pas des héros-victimes. | 0.20 |
| 11. Départ | Vassilissa quitte la maison pour aller chez Baba Yaga (↑). Le départ est clairement marqué avec le voyage à travers la forêt. | 0.95 |
| 12. Première fonction du donateur | La mère mourante donne des instructions et confie la poupée (D³ - une personne mourante demande la prestation d'un service). Baba Yaga met Vassilissa à l'épreuve avec des tâches ménagères impossibles (D¹). | 0.95 |
| 13. Réaction du héros | Vassilissa rend service à la personne décédée (sa mère) en gardant la poupée (E³). Elle résiste aux épreuves de Baba Yaga grâce à la poupée (E¹). Elle fait preuve de prudence en ne posant pas de questions sur l'intérieur. | 0.95 |
| 14. Réception de l'objet magique | La poupée est reçue de la mère mourante (F¹ - transfert direct). C'est un agent magique qui aide Vassilissa tout au long du conte. Le crâne aux yeux ardents est aussi donné par Baba Yaga (F¹). | 0.95 |
| 15. Déplacement | Vassilissa voyage à travers la forêt jusqu'à la hutte de Baba Yaga. Elle est guidée par le chemin (G²/G³). Le retour est éclairé par le crâne (G³). | 0.85 |
| 16. Combat | Il n'y a pas de combat direct entre Vassilissa et un agresseur. Les épreuves de Baba Yaga sont des tâches, pas un combat. | 0.10 |
| 17. Marque | Vassilissa ne reçoit pas de marque physique. Pas de blessure ni d'objet de reconnaissance donné pendant un combat. | 0.10 |
| 18. Victoire | Vassilissa "vainc" Baba Yaga en accomplissant les tâches et en étant chassée avec le feu demandé. C'est une forme de victoire par accomplissement plutôt que par combat. La marâtre et ses filles sont consumées par le crâne (I⁵ - tué sans combat). | 0.85 |
| 19. Réparation | Le méfait initial est réparé : la marâtre et ses filles sont détruites par le crâne (K⁴ - résultat direct des actions précédentes). Vassilissa est libérée de ses tourmenteuses. | 0.95 |
| 20. Retour | Vassilissa retourne chez elle avec le crâne, puis va en ville (↓). Le retour est clairement marqué. | 0.90 |
| 21. Poursuite | Il n'y a pas de poursuite. Baba Yaga laisse partir Vassilissa. | 0.05 |
| 22. Secours | Pas de secours nécessaire car pas de poursuite. | 0.05 |
| 23. Arrivée incognito | Vassilissa arrive chez une vieille femme en ville et vit modestement, sans révéler sa vraie nature (o). Elle sert comme "fille adoptive". | 0.85 |
| 24. Imposture | Il n'y a pas de faux héros présentant des prétentions non fondées dans ce conte. | 0.05 |
| 25. Tâche difficile | Le tsar demande que des chemises soient cousues dans la toile extraordinaire - aucun tailleur n'y parvient (M). C'est une tâche de fabrication. Les tâches de Baba Yaga (trier le blé, les graines de pavot) sont aussi des tâches difficiles, mais elles relèvent plutôt de D¹. | 0.85 |
| 26. Accomplissement | Vassilissa accomplit la tâche de coudre les chemises (N). Elle avait aussi accompli les tâches de Baba Yaga. | 0.90 |
| 27. Reconnaissance | Le tsar reconnaît la valeur de Vassilissa quand elle livre les chemises, "soigneusement vêtue et apprêtée" (Q). Il reconnaît qu'elle est l'auteure de la toile et des chemises. | 0.85 |
| 28. Découverte | Il n'y a pas de faux héros à démasquer. La marâtre a déjà été punie. | 0.10 |
| 29. Transfiguration | Vassilissa se présente "soigneusement vêtue et apprêtée" au palais (T³ - nouveaux vêtements). Elle passe de servante/orpheline à tsarine. | 0.80 |
| 30. Châtiment | La marâtre et ses filles sont consumées par les yeux du crâne (U). C'est un châtiment clair et définitif. | 0.95 |
| 31. Mariage | Le tsar tombe amoureux de Vassilissa et l'épouse (W**). Elle devient tsarine. Le père revient et vit auprès d'elle. Fin heureuse classique. | 0.95 |

---

## Partie 2 : Séquence résultante

Fonctions avec score ≥ 0.85 :

**01, 02, 06, 07, 08, 09, 11, 12, 13, 14, 15, 18, 19, 20, 23, 25, 26, 27, 30, 31**
```

**Metrics:** {'contains': 0.0}
