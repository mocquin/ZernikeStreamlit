import streamlit as st
from mocapy.zernike import Zernike

# Set wide layout
st.set_page_config(layout="wide")

# Title and introductory header
st.title('Zernike Polynomials')
st.header('Recap')
st.write('Let\'s review what we learned about radial and angular polynomials:')

# Radial polynomial section
st.subheader('Radial Polynomials')
st.latex(r"""
    r_n^m(\rho) =
    \begin{cases}
        \sum_{i=0}^{(n-m)/2} \frac{(-1)^i (n-i)!}{i!(\frac{n+m}{2}-i)!(\frac{n-m}{2}-i)!}\rho^{n-2i} & \text{for $n-m$ even}\\
        0 & \text{for $n-m$ odd}\\
    \end{cases}
""")
st.latex(r"r_n^{m} \cdot r_{n'}^{m} = \int_0^1 r_n^m(\rho) r_{n'}^m(\rho) \rho d\rho = \frac{\delta_{n,n'}}{2n+2}")
st.write('Using the normalization coefficient:')
st.latex(r'R_n^m = N_n r_n^m = \sqrt{2n+2} r_n^m')
st.latex(r"R_n^m \cdot R_{n'}^m = \int_0^1 R_n^m(\rho) R_{n'}^m(\rho) \rho d\rho = \delta_{nn'}")

# Angular polynomial section
st.subheader("Angular Polynomials")
st.latex(r"""
         a_m(\theta) =
\begin{cases}
\sin(-m \theta) & \text{if $m<0$}\\
\cos(m \theta)  & \text{if $m>0$}\\
1 & \text{if $m=0$}\\
\end{cases}
""")
st.latex(r"a_{m} \cdot a_{m'} = \int_0^{2\pi} a_m(\theta) a_{m'}(\theta) d\theta = \delta_{mm'}(1+\delta_{m0}) \pi")
st.write('Using the normalization coefficient:')
st.latex(r'A_m = N_m a_m = \frac{a_m}{\sqrt{(1+\delta_{m0}) \pi}}')
st.write('Then:')
st.latex(r"A_m \cdot A_{m'} = \int_0^{2\pi} A_m(\theta) A_{m'}(\theta) d\theta = \delta_{mm'}")

# Zernike polynomial definition and orthogonality
st.header('Definition and Orthogonality of Zernike Polynomials')
st.write('Zernike polynomials are indexed using two indices, $n$ and $m$, to combine the radial and angular polynomials:')
st.latex(r"z_n^m(\rho, \theta) = r_n^m(\rho) a_m(\theta)")
st.write('The dot product is then:')
st.latex(r"z_n^m \cdot z_{n'}^{m'} = \delta_{nn'} \delta_{mm'}\frac{(1+\delta_{m0})\pi}{2n+2} = \delta_{nmn'm'} \frac{(1+\delta_{m0})\pi}{2n+2}")
st.latex(r"Z_n^m \cdot Z_{n'}^{m'} = \delta_{nmn'm'}")

# Leading normalization coefficient
st.write('The leading normalization coefficient is:')
st.latex(r"N_n^m = N_n \cdot N_m = \sqrt{2n+2} \cdot \frac{1}{\sqrt{(1+\delta_{m0})\pi}} = \sqrt{ \frac{ 2n+2 }{(1+\delta_{m0})\pi}}")

# Zernike polynomial creation example
st.write('To create a Zernike polynomial:')
st.code(r"""
>>> z = Zernike(4, 2)
>>> z
Zernike(n=4, m=2, ortho_norm=False : 4*rho**4*cos(2*theta) - 3*rho**2*cos(2*theta))
""")
st.write('The Zernike class has attributes for the underlying radial and angular polynomials, available as `R` and `A`:')
st.code(r"""
>>> z.R
<Radial(n=4, m=2, ortho_norm=False) : 4*rho**4 - 3*rho**2>     
>>> z.A
<Angular(m=2, ortho_norm=False : cos(2*theta))
""")
st.write(r'To compute the Zernike polynomial value, use polar coordinates $(\rho, \theta)$ or Cartesian $(x, y)$ with `.cart()`:')
st.code(r"""
>>> z(0.5, pi/2)
0.5
""")

# Zernike Inspector Section
st.header("Zernike Inspector")

# Columns for Zernike parameters
col1, col2, col3 = st.columns(3)

with col1:
    n = st.number_input("n", min_value=0, max_value=10, value=0, key='n_input')
with col2:
    m = st.number_input("m", min_value=0, max_value=10, value=0, key='m_input')
with col3:
    ortho_norm = st.checkbox("Orthonormalize")

# Create Zernike instance
z = Zernike(n, m, ortho_norm)

# Plotting each component in 3 columns
col1, col2, col3 = st.columns(3)

with col1:
    fig = z.R.plot_3d_plotly(False)
    fig.update_layout(title='Radial Component')
    st.plotly_chart(fig, use_container_width=True)

with col2:
    fig = z.A.plot_3d_plotly(False)
    fig.update_layout(title='Angular Component')
    st.plotly_chart(fig, use_container_width=True)

with col3:
    fig = z.plot_3d_plotly(False)
    fig.update_layout(title='Zernike Polynomial')
    st.plotly_chart(fig, use_container_width=True)

# Indexing schemes section
st.header('Indexing Schemes')
st.write("Several indexing schemes have been developed to order Zernike polynomials as a sequence, which is useful for readability and control flow (e.g., looping over the first N polynomials).")

# Properties Section
st.header('Properties')
st.write('Zernike polynomials provide various useful properties.')

# Derivatives Subsection
st.subheader("Derivatives")
st.latex(r"""
\frac{\partial Z_n^m}{\partial x}(\rho, \theta) = N_n^m \left[ \frac{dR_n^{|m|}}{d\rho} A^{|m|}(\theta) \cos(\theta) - \frac{R_n^{|m|}}{\rho} \frac{dA^{|m|}}{d\theta} \sin(\theta) \right] \\
\frac{\partial Z_n^m}{\partial y}(\rho, \theta) = N_n^m \left[ \frac{dR_n^{|m|}}{d\rho} A^{|m|}(\theta) \sin(\theta) + \frac{R_n^{|m|}}{\rho} \frac{dA^{|m|}}{d\theta} \cos(\theta) \right]
""")
st.markdown(r"with $N_n^m=\sqrt{\frac{2(n+1)}{1+\delta_{0m}}}$")


# Display a summary dataframe of Zernike polynomials
st.write("Summary of Zernike Polynomials:")
st.dataframe(Zernike.summup())
