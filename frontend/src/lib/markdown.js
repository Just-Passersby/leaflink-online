import { Marked } from 'marked';
import DOMPurify from 'dompurify';

function makeWikilinkExtension(titleMap) {
	return {
		name: 'wikilink',
		level: 'inline',
		start(src) {
			return src.indexOf('[[');
		},
		tokenizer(src) {
			const match = src.match(/^\[\[([^\]]+)\]\]/);
			if (match) {
				return { type: 'wikilink', raw: match[0], title: match[1].trim() };
			}
		},
		renderer(token) {
			const id = titleMap[token.title];
			const href = id
				? `/notes/${id}`
				: `/search?q=${encodeURIComponent(token.title)}`;
			return `<a href="${href}" class="wikilink">[[${token.title}]]</a>`;
		}
	};
}

export function renderMarkdown(content, titleMap = {}) {
	const instance = new Marked();
	instance.use({ extensions: [makeWikilinkExtension(titleMap)] });
	return DOMPurify.sanitize(String(instance.parse(content || '')));
}
