#%% packages
from transformers import pipeline
import pandas as pd

#%% Classifier
classifier = pipeline(task="zero-shot-classification", model="facebook/bart-large-mnli")
# %% Data Preparation
# first example: Jane Austen: Pride and Prejudice  (romantic novel)
# second example: Lewis Carroll: Alice's Adventures in Wonderland (fantasy novel)
# third example: Arthur Conan Doyle "The Return of Sherlock Holmes" (crime novel)
titles = ["Pride and Prejudice", "Alice im Wunderland", "Die Rückkehr des Sherlock Holmes"]
documents = [
    "Walt Whitman macht irgendwo eine feine und gerechte Unterscheidung zwischen „Liebe aus Gewohnheit“ und „persönlicher Liebe“. Diese Unterscheidung gilt für Bücher ebenso wie für Männer und Frauen; und bei den nicht sehr zahlreichen Autoren, die Gegenstand persönlicher Zuneigung sind, bringt sie eine merkwürdige Konsequenz mit sich. Es gibt viel größere Unterschiede in Bezug auf ihr bestes Werk als bei jenen anderen, die „aus Gewohnheit“ geliebt werden, also aus Konvention und weil man meint, es sei richtig und angebracht, sie zu lieben. Und in der Sekte – ziemlich groß und doch ungewöhnlich erlesen – der Austenianer oder Janiten gäbe es wahrscheinlich Anhänger für den Vorrang fast jedes Romans. Für manche verdunkeln die herrliche Frische und der Humor von Northanger Abbey, seine Vollständigkeit, Ausgereiftheit und sein Schwung die unbestreitbaren kritischen Tatsachen, dass sein Umfang gering ist und sein Plan letztlich eine Parodie oder ein Burleske ist, eine Art, in der es schwer ist, zur ersten Klasse zu gehören.",
    "Alice fängt an, es sehr leid zu sein, neben ihrer Schwester am Ufer zu sitzen und nichts zu tun zu haben: ein- oder zweimal hatte sie in das Buch hineingeschaut, das ihre Schwester las, aber es hatte weder Bilder noch Gespräche, und wozu taugt ein Buch, dachte Alice, „ohne Bilder oder Gespräche?“ Daher überlegte sie in Gedanken (so gut sie konnte, denn der heiße Tag machte sie sehr schläfrig und dösig), ob es sich lohnen würde, eine Gänseblümchenkette zu machen, auch wenn es mit dem Aufstehen und Pflücken der Gänseblümchen verbunden wäre. Da rannte plötzlich ein weißes Kaninchen mit rosa Augen dicht an ihr vorbei.",
    "Es war im Frühjahr 1894, als ganz London an dem Mord an dem ehrenwerten Ronald Adair unter höchst ungewöhnlichen und unerklärlichen Umständen interessiert war und die feine Gesellschaft bestürzt wurde. Die Öffentlichkeit hat bereits jene Einzelheiten der Tat erfahren, die bei den polizeilichen Ermittlungen ans Licht kamen; doch einiges wurde damals zurückgehalten, da der Fall für die Anklage so überwältigend klar war, dass es nicht nötig war, alle Fakten vorzubringen. Erst jetzt, nach fast zehn Jahren, darf ich jene fehlenden Verknüpfungen liefern, welche die gesamte Kette dieses bemerkenswerten Falls ausmachen. Das Verbrechen war an sich schon interessant, doch war dieses Interesse für mich nichts im Vergleich zur unfassbaren Folge, die mir den stärksten Schock und das größte Erstaunen meines abenteuerlichen Lebens verschaffte. Selbst jetzt, nach dieser langen Zeit, durchläuft mich ein Zittern, wenn ich daran denke, und ich spüre abermals jene plötzliche Woge von Freude, Erstaunen und Ungläubigkeit, die meinen Geist vollständig durchflutete. Ich sage hier der Öffentlichkeit, die von Zeit zu Zeit Interesse an jenen Einblicken gezeigt hat, die ich über die Gedanken und Taten eines höchst bemerkenswerten Mannes gegeben habe, dass sie mir keine Vorwürfe machen soll, wenn ich mein Wissen nicht mitgeteilt habe; ich hätte dies als meine erste Pflicht betrachtet, wäre ich nicht durch ein ausdrückliches Verbot seinerseits daran gehindert worden, das erst am dritten des vergangenen Monats aufgehoben wurde."
             ]
        
candidate_labels=["Romantik", "Fantasy", "Krimi"]
#%% classify documents
res = classifier(documents, candidate_labels = candidate_labels)


#%% visualize results
pos = 2
pd.DataFrame(res[pos]).plot.bar(x='labels', y='scores', title=titles[pos])
# %%
