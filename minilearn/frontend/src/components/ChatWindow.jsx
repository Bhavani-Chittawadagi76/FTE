import CourseCard from "./CourseCard";
import SearchBar from "./SearchBar";

function ChatWindow({ message, setMessage, onSubmit, loading, response, courses, onDetails, onEnroll }) {
  return (
    <section className="chat-panel">
      <div className="chat-panel-header">
        <div>
          <p className="eyebrow">Learning discovery</p>
          <h1>Find your next skill</h1>
          <p className="panel-subtitle">Search the catalog, compare courses, and build your learning path.</p>
        </div>
        <div className="status-pill"><span className="status-dot" /> Agent ready</div>
      </div>
      <SearchBar message={message} onChange={setMessage} onSubmit={onSubmit} loading={loading} />
      <div className="results-header">
        <div>
          <p className="eyebrow">Course catalog</p>
          <h2>{courses.length ? `${courses.length} courses found` : "Explore the catalog"}</h2>
        </div>
        {response && <p className="response-note">{response}</p>}
      </div>
      {courses.length ? (
        <div className="course-grid">
          {courses.map((course) => (
            <CourseCard key={course.learningId} course={course} onDetails={onDetails} onEnroll={onEnroll} />
          ))}
        </div>
      ) : (
        <div className="empty-state">
          <div className="empty-icon">✦</div>
          <h3>What would you like to learn?</h3>
          <p>Try “machine learning”, “Python”, or “popular courses”.</p>
        </div>
      )}
    </section>
  );
}

export default ChatWindow;
