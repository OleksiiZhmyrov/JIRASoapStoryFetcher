
class StoryCard:

    def __init__(self, index, number, summary, description, assignee, tester, reporter, points, epic):
        self.number = number
        self.summary = summary
        self.description = description
        self.assignee = assignee
        self.tester = tester
        self.reporter = reporter
        self.points = points
        self.epic = epic
        self.column = (6, 0)[index % 2 == 0]
        self.row = index / 2 * 15

    def render(self, sheet):
        sheet.write_merge(r1=self.row+0, c1=self.column+0, r2=self.row+3, c2=self.column+0, label=self.number)
        sheet.write_merge(r1=self.row+0, c1=self.column+1, r2=self.row+3, c2=self.column+5, label=self.summary)
        sheet.write_merge(r1=self.row+4, c1=self.column+0, r2=self.row+10, c2=self.column+5, label=self.description)
        sheet.write_merge(r1=self.row+11, c1=self.column+0, r2=self.row+11, c2=self.column+1, label="Assignee:")
        sheet.write_merge(r1=self.row+11, c1=self.column+2, r2=self.row+11, c2=self.column+4, label=self.assignee)
        sheet.write_merge(r1=self.row+12, c1=self.column+0, r2=self.row+12, c2=self.column+1, label="Tester:")
        sheet.write_merge(r1=self.row+12, c1=self.column+2, r2=self.row+12, c2=self.column+4, label=self.tester)
        sheet.write_merge(r1=self.row+13, c1=self.column+0, r2=self.row+13, c2=self.column+1, label="Reporter:")
        sheet.write_merge(r1=self.row+13, c1=self.column+2, r2=self.row+13, c2=self.column+4, label=self.reporter)
        sheet.write_merge(r1=self.row+11, c1=self.column+5, r2=self.row+13, c2=self.column+5, label=self.points)
        sheet.write_merge(r1=self.row+14, c1=self.column+0, r2=self.row+14, c2=self.column+5, label=self.epic)

        return sheet
