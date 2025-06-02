def split_story(story, max_words=46):
    words = story.split()
    parts = []
    current_part = []
    current_word_count = 0

    for word in words:
        if current_word_count + len(current_part) + 1 <= max_words:  # +1 for the space
            current_part.append(word)
            current_word_count += 1
        else:
            parts.append(" ".join(current_part))
            current_part = [word]
            current_word_count = 1
    if current_part:
        parts.append(" ".join(current_part))
    return parts

story_text = '''YFree download at http://rahulmehta
story_parts = split_story(story_text)

for part in story_parts:
    print(part)

