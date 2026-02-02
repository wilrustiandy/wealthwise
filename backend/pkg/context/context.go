package context

type ContextKey int

const (
	RequestID ContextKey = iota
)

var ContextKeys = map[ContextKey]string{
	RequestID: "RequestID",
}
