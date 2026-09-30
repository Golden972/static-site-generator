class HTMLNode:
    def __init__(
        self,
        tag: str | None = None,
        value: str | None = None,
        children: list["HTMLNode"] | None = None,
        props: dict[str, str] | None = None
    ) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("to_html method not implemented")

    def props_to_html(self) -> str:
        props_as_html: str = ""
        if not self.props:
            return props_as_html
        for attribute, value in self.props.items():
            props_as_html += f' {attribute}="{value}"'
        return props_as_html

    def __repr__(self) -> str:
        return f"HTMLNode: tag={self.tag}, value={self.value}, children={self.children}, props={self.props}"
