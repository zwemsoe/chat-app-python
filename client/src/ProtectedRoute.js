import { Route, Redirect } from "react-router-dom";

export default function ProtectedRoutes({
  component: Component,
  template,
  auth,
  ...rest
}) {
  const switchRoute = () => {
    switch (template) {
      case "afterLogin":
        return (
          <Route
            {...rest}
            render={(props) => {
              return auth ? (
                <Component {...props} />
              ) : (
                <div>Page Not Found</div>
              );
            }}
          />
        );

      case "beforeLogin":
        return (
          <Route
            {...rest}
            render={(props) => {
              return !auth ? (
                <Component {...props} />
              ) : (
                <Redirect
                  to={{
                    pathname: "/",
                    state: {
                      from: props.location,
                    },
                  }}
                />
              );
            }}
          />
        );
      default:
        return;
    }
  };

  return <>{switchRoute()}</>;
}
