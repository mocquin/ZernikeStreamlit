import streamlit as st
from mocapy.zernike import Angular
import sympy as sp

# Title of the app
st.title("Angular Polynomials")

# Caching the 3D plot function
@st.cache_resource
def get_angular_plot(m):
    fig = Angular(m).plot_3d_plotly()
    fig.update_layout(title=f"Angular(m={m})")
    return fig

# Interactive slider for m parameter in intro plot
st.header("Intro Plot")
m_value = st.slider("Select value of m", min_value=-10, max_value=10, value=5)
fig = get_angular_plot(m_value)
st.plotly_chart(fig, use_container_width=True)

# Definition section
st.header('Definition')
st.write(r"""Angular polynomials are, like radial polynomials, 1d functions and are indexed using a single integer $m$:""")
st.latex(r"""
a_m(\theta) =
\begin{cases}
\sin(-m \theta) & \text{if $m<0$}\\
\cos(m \theta)  & \text{if $m>0$}\\
1 & \text{if $m=0$}\\
\end{cases}
""")

# Code example for creating Angular instance
st.write('To create an Angular instance:')
st.code(r"""
>>> a = Angular(3)
>>> a
<Angular(m=3, ortho_norm=False : cos(3*theta))
""")

# Explanation of analytical expression
st.write('The analytical expression is computed using sympy (e.g., `cos(3*theta)`) and is accessible via `.expr`. To plot the angular function as a 2D:')
st.code(r"""
a.plot_3d_plotly()
""")

# Displaying an example 3D plot of Angular(3)
fig_example = Angular(3).plot_3d_plotly()
fig_example.update_layout(title='Angular(3) Example Plot')
st.plotly_chart(fig_example, use_container_width=True)

# Interactive Angular Inspector
st.header("Angular Inspector")
st.write('Experiment with the m index and the normalization options:')

# Columns for inspector controls and results
col1, col2 = st.columns(2)

with col1:
    m_input = st.number_input("m", min_value=-10, max_value=10, value=0, key='a_input')
    ortho_norm = st.checkbox("Orthonormalize", key='ortho_norm')
    
    # Attempt to create Angular instance with user inputs and display its properties
    try:
        angular_instance = Angular(m_input, ortho_norm=ortho_norm)
        st.code(f">>> a = Angular(m={m_input}, ortho_norm={ortho_norm})\n>>> a\n{repr(angular_instance)}")
        expr_str = fr'a^{{{m_input}}}(\theta) = {sp.latex(angular_instance._expr)}'
        st.latex(expr_str)
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

with col2:
    # Try to plot the Angular function
    try:
        fig_inspector = angular_instance.plot_3d_plotly()
        fig_inspector.update_layout(title=f"Angular(m={m_input}) 3D Plot")
        st.plotly_chart(fig_inspector, use_container_width=True)
    except Exception as e:
        st.error(f"Plotting error: {str(e)}")

# Normalization and orthogonality section
st.header('Normalization and Orthogonality')
st.markdown(r"""
    The product of two polynomials over the interval $[0, 2\pi]$ reveals orthogonality based on the $m$ index:
    """)

st.latex(r"a_{m} \cdot a_{m'} = \int_0^{2\pi} a_m(\theta)a_{m'}(\theta) d\theta = \delta_{mm'}(1+\delta_{m0})\pi")

# Example code for orthogonality and normalization
st.write('By default, angular polynomials are orthogonal:')
st.code(r"""
>>> a_m3 = Angular(-3)
>>> a_4 = Angular(4)
>>> a_m3.dot(a_4)  # Outputs 0, showing orthogonality
>>> a_m3.dot(a_m3)  # Outputs π, indicating normalization
""")

st.write('To make them orthonormal, use `ortho_norm=True`:')
st.code(r"""
>>> a_m3 = Angular(-3, ortho_norm=True)
>>> a_m3.dot(a_m3)
1
""")

# Explanation of normalized polynomials with alternate definition
st.write('Another definition is possible by adding a leading coefficient to make the polynomials orthonormal. Noting them as `A_m`:')
st.latex(r'A_m = N_m a_m = \frac{a_m}{\sqrt{(1+\delta_{m0})}\pi}')
st.write('Then:')
st.latex(r"A_m \cdot A_{m'} = \int_0^{2\pi} A_m(\theta) A_{m'}(\theta) d\theta = \delta_{mm'}")
st.write("The `ortho_norm` argument controls whether a polynomial is self-normalized.")

# Display a summary dataframe of Angular polynomials
st.write("Summary of Angular Polynomials:")
st.dataframe(Angular.summup())
