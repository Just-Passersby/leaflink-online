import { marked } from 'marked';
import DOMPurify from 'dompurify';

const wikilinkExtension = {
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
		return `<a href="/search?q=${encodeURIComponent(token.title)}" class="wikilink">[[${token.title}]]</a>`;
	}
};

marked.use({ extensions: [wikilinkExtension] });

export function renderMarkdown(content) {
	return DOMPurify.sanitize(String(marked.parse(content || '')));
}
