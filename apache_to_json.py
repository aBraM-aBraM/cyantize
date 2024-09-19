import click
import json


# Converts this https://svn.apache.org/repos/asf/httpd/httpd/trunk/docs/conf/mime.types to json and remove
# redundant values. CONVERTS IN PLACE


@click.command()
@click.argument("apache-mime-types", type=click.Path(exists=True, dir_okay=False))
def main(apache_mime_types):
    with open(apache_mime_types) as f:
        raw_lines = f.readlines()
    remove_comments = [line.strip() for line in raw_lines if not line.startswith("#")]
    extension_to_mime = {}
    for line in remove_comments:
        line_split = line.split()
        mime = line_split[0]
        extensions = line_split[1:]
        for extension in extensions:
            extension_to_mime[extension] = mime
    assert (
        len(set(extension_to_mime.keys()).difference(set(extension_to_mime.keys())))
        == 0
    )

    print(extension_to_mime)

    with open(apache_mime_types, "w") as f:
        json.dump(extension_to_mime, f)


if __name__ == "__main__":
    main()
