from xcodefy.library.serialization.encoder import Encoder
from xcodefy.library.serialization.printing_density import PrintingDensity
from xcodefy.library.serialization.values.comment import Comment
from xcodefy.library.serialization.values.comment_style import CommentStyle


def test_values_are_appended_in_order():
    encoder = Encoder()
    container = encoder.ordinal()
    container.put(1)
    container.put("a")
    assert container.finish().to_python() == [1, "a"]


def test_an_element_density_is_recorded_against_the_element_path():
    encoder = Encoder()
    container = encoder.ordinal()
    container.put([1], PrintingDensity.COMPACT)
    assert encoder.densities[container.path.appending_index(0)] is PrintingDensity.COMPACT


def test_comments_are_interleaved_with_values():
    container = Encoder().ordinal()
    container.add_comment(Comment(CommentStyle.LINE, "note"))
    container.put(1)
    entries = container.finish().content
    assert [entry.is_value for entry in entries] == [False, True]
