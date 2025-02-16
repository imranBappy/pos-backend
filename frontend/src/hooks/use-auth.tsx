import { JWT_TOKEN_KEY, ROLE_KEY } from "@/constants/auth.constants";
import { USER_TYPE } from "@/graphql/accounts";
import { ME_QUERY } from "@/graphql/accounts/queries";
import authVerify, { AuthVerifyResult } from "@/lib/auth";
import { useQuery } from "@apollo/client";
import { useRouter } from "next/navigation";
import { useState, useEffect } from "react"



const useAuth = () => {
    const [isAuthenticated, setIsAuthenticated] = useState(false)
    const [isLoading, setIsLoading] = useState(true)
    const [user, setUser] = useState<USER_TYPE | null>(null)
    const authData: AuthVerifyResult = authVerify()
    const router = useRouter()

    const logout = () => {
        localStorage.removeItem(JWT_TOKEN_KEY)
        localStorage.removeItem(ROLE_KEY)
        setIsAuthenticated(false)
        setIsLoading(false)
        router.push("/login")
    }

    useQuery(ME_QUERY, {
        onCompleted(data) {
            const { email, name, role, photo,id } = data.me
            setUser({
                email: email,
                name: name,
                role: role,
                photo: photo,
                id: id
            })
        },
        onError() {
            logout()
        }
    })


    useEffect(() => {
        if ('error' in authData) {
            setIsAuthenticated(false)
        } else {
            setIsAuthenticated(true)
        }
        setIsLoading(false)
    }, [authData])

    if (isAuthenticated) {
        return {
            isAuthenticated: isAuthenticated,
            isLoading: isLoading,
            user: user,
            logout: logout
        }
    }
    if (!isAuthenticated) {
        return {
            isAuthenticated: isAuthenticated,
            isLoading: isLoading,
            user: null,
            logout: logout
        }
    }

}

export default useAuth