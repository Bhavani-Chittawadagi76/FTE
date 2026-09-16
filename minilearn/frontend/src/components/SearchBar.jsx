function SearchBar({ message, onChange, onSubmit, loading }) {
  return (
    <form className="search-bar" onSubmit={onSubmit}>
      <div className="search-field">
        <span className="search-icon" aria-hidden="true">⌕</span>
        <input
          type="text"
          value={message}
          onChange={(event) => onChange(event.target.value)}
          placeholder="Search courses, skills, or topics"
          aria-label="Search courses"
        />
      </div>
      <button className="send-button" type="submit" disabled={loading || !message.trim()}>
        {loading ? "Searching..." : "Search"}
      </button>
    </form>
  );
}

export default SearchBar;
