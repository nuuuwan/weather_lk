class Markdown:
    TABLE_DELIM_COLUMN = ' | '

    def build_row(values):
        return (
            Markdown.TABLE_DELIM_COLUMN
            + Markdown.TABLE_DELIM_COLUMN.join(values)
            + Markdown.TABLE_DELIM_COLUMN
        )

    def build_table(keys, values_list):
        sep = [(' ---- ' if 'id' in key else ' ---: ') for key in keys]
        lines = [
            Markdown.build_row(keys),
            Markdown.build_row(sep),
        ]
        for values in values_list:
            lines.append(Markdown.build_row(values))
        return lines
